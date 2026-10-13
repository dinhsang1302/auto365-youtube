"""Assemble editor-reviewed sections; central public-copy and signature policy.

No ASR, browser, paid service or publishing calls. Facts remain in job sources;
this module formats verified inputs and never invents a narrative or permission.
"""
import argparse
import hashlib
import re
from pathlib import Path
from youtube_editorial import read_json, write_json, job_directory, validate_manual_chapters, workspace_root, project_path


def signature_for(profile, category):
    phone = profile['signatures'][category]['phone']
    signature = profile['signature_template'].format(phone=phone)
    expected = (f"☎ Tư vấn: {phone}\n"
                f"☎ Hotline nhập sỉ: {profile['brand']['wholesale_hotline']}\n"
                f"☎ Hotline phản ánh chất lượng dịch vụ: {profile['brand']['quality_hotline']}")
    if expected not in signature or signature.count(profile['signature_brand_line']) != 1:
        raise ValueError('Channel template has incorrect hotline labels, order, numbers or repeated signature.')
    return signature


def signature_errors(description, profile, category):
    signature = signature_for(profile, category)
    errors = []
    if description.count(signature) != 1 or description.count(profile['signature_brand_line']) != 1:
        errors.append('Description must contain exactly one current category signature.')
    outside = description.replace(signature, '')
    if re.search(r'(?:☎\s*)?(?:Tư vấn|Hotline)\s*:', outside, re.I) or 'AUTO365 |' in outside:
        errors.append('Description contains an extra or legacy signature/hotline block.')
    known = [phone.strip() for entry in profile['signatures'].values()
             for phone in entry['phone'].split(' - ')]
    known += [profile['brand']['wholesale_hotline'], profile['brand']['quality_hotline'],
              profile['brand']['superseded_phone_not_for_current_signature']]
    if any(re.search(r'(?<!\d)' + r'[\s.\-]*'.join(re.sub(r'\D', '', phone)) + r'(?!\d)', outside)
           for phone in known):
        errors.append('A routed or obsolete phone number occurs outside the canonical signature.')
    return errors


def public_copy_errors(*texts):
    """Apply public-only rules; never remove commercial fields from source data."""
    errors = []
    for text in texts:
        if re.search(r'\bVAT\b|thuế\s+giá\s+trị\s+gia\s+tăng', text or '', re.I):
            errors.append('Public copy must not mention VAT; preserve tax facts internally.')
        if re.search(r'\[(?:TODO|PLACEHOLDER|cần\s+(?:xác minh|bổ sung)|timestamp\s+ước lượng|phạm vi mỗi đèn cần nghe lại)[^\]]*\]|ghi\s+chú\s+nội\s+bộ|\{(?:phone|amount_vnd|unit)\}', text or '', re.I):
            errors.append('Public copy contains an internal note or placeholder.')
    return errors


def permission_for(job, action, revision=None, content_sha256=None):
    """Report job-specific authority; this function cannot grant new permission."""
    request = job.get('action_request')
    if request:
        target_matches = request.get('channel_id') == job.get('channel_id')
        if request.get('video_id'):
            target_matches = target_matches and request['video_id'] == job.get('video_id')
        if action == 'edit_description':
            target_matches = (target_matches and bool(revision) and bool(content_sha256)
                              and revision == request.get('revision')
                              and content_sha256 == request.get('approved_description_sha256'))
        return bool(target_matches and request.get('mode') != 'prepare_only'
                    and request.get('source') and action in request.get('authorized_actions', []))
    # Historical publication permission is evidence of an old action, not
    # authority to act in a new turn. Record the latest specific instruction.
    return False


def description_sha256(text):
    """Hash approved UTF-8 content, not a summary or an estimated character count."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def render_price(price, category='lighting'):
    if not price:
        return ''
    if not price.get('verified') or not price.get('source') or price.get('scope') != 'product_only':
        raise ValueError('A product reference price needs a verified source and product-only scope.')
    amount = price.get('amount_vnd')
    if type(amount) is not int or amount <= 0 or not price.get('unit'):
        raise ValueError('Price amount and unit must be known; do not invent them.')
    amount_text = f'{amount:,}'.replace(',', '.')
    label = 'Giá bộ đèn tham khảo' if category == 'lighting' else 'Giá sản phẩm tham khảo'
    return (f"{label}: {amount_text} đồng/{price['unit']}. "
            'Liên hệ Auto365 để được tư vấn cấu hình và báo giá hoàn thiện theo xe.')


def assemble(brief, profile):
    """Each body section is written and source-reviewed by the editor, not templated."""
    if brief.get('channel_id') and brief['channel_id'] != profile['channel_id']:
        raise ValueError('Description brief belongs to a different target channel.')
    opening = brief.get('opening_lines', [])
    if not opening or any(not isinstance(line, str) or not line.strip() for line in opening):
        raise ValueError('Supply a video-specific opening; use the length justified by this video.')
    # Templates suggest questions and depth; they never create claims or require
    # every narrative purpose. Do not truncate useful explanation to a set length.
    sections = brief.get('narrative_sections')
    if sections is not None:
        if brief.get('paragraphs'):
            raise ValueError('Use narrative_sections or legacy paragraphs, not both.')
        body = []
        for section in sections:
            if (not isinstance(section, dict) or not isinstance(section.get('text'), str)
                    or not section['text'].strip() or not section.get('purpose') or not section.get('evidence')):
                raise ValueError('Each included narrative section needs complete text, purpose and reviewed evidence.')
            body.append(section['text'].strip())
    else:
        body = [p.strip() for p in brief.get('paragraphs', []) if p.strip()]
    blocks = ['\n'.join(opening)] + body
    if brief.get('price'):
        blocks.append(render_price(brief['price'], brief['category']))
    warranty = brief.get('warranty')
    if warranty:
        if not warranty.get('verified') or not warranty.get('source') or not warranty.get('text'):
            raise ValueError('Warranty text needs a verified source; otherwise omit this section.')
        blocks.append(warranty['text'])
    for link in brief.get('links', []):
        if not link.get('verified') or not link.get('label') or not link.get('url', '').startswith('https://'):
            raise ValueError('Each included link needs a checked destination and a clear label.')
        blocks.append(link['label'] + '\n' + link['url'])
    if brief.get('cta'):
        blocks.append(brief['cta'])
    chapters = brief.get('chapters', [])
    if chapters:
        errors = validate_manual_chapters(chapters, brief['duration_seconds'])
        if errors:
            raise ValueError('; '.join(errors))
        blocks.append('TIMELINE CHI TIẾT:\n' + '\n'.join(
            f"{int(c['start_seconds'])//60:02}:{int(c['start_seconds'])%60:02} {c['title']}"
            for c in chapters))
    signature = signature_for(profile, brief['category'])
    blocks.append(signature)
    if brief.get('hashtags'):
        blocks.append(' '.join(brief['hashtags']))
    description = '\n\n'.join(blocks)
    errors = public_copy_errors(description, brief.get('pinned_comment_proposal', ''))
    errors.extend(signature_errors(description, profile, brief['category']))
    if len(description) > 5000:
        errors.append('Description exceeds the YouTube character limit.')
    if errors:
        raise ValueError('; '.join(errors))
    return description


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--brief', required=True)
    parser.add_argument('--profile', required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--workspace', help='Project root; defaults to cwd ancestry, not script location')
    args = parser.parse_args()
    output = job_directory(args.output_dir, args.workspace)
    destination = output / 'description.after.txt'
    if destination.exists():
        raise SystemExit('Output exists; preserve it and create a new revision directory.')
    root = workspace_root(args.workspace)
    brief = read_json(project_path(args.brief, root))
    profile = read_json(project_path(args.profile, root))
    description = assemble(brief, profile)
    destination.write_text(description, encoding='utf-8')
    write_json(output / 'public-copy-check.json', {
        'state': 'PUBLIC_COPY_STRUCTURAL_CHECK_PASSED',
        'source_review': 'Editor verifies facts; formatter only checks supplied flags and structure.',
        'remote_actions': [], 'characters': len(description)})


if __name__ == '__main__':
    main()
