#!/usr/bin/env python3
import os, re
from datetime import datetime, timedelta

source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'source')

files = []
for root, dirs, fnames in os.walk(source_dir):
    for fn in fnames:
        if fn.endswith('.md'):
            fp = os.path.join(root, fn)
            with open(fp, 'r') as f:
                content = f.read()
            fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if fm_match:
                fm = fm_match.group(1)
                has_date = re.search(r'^date:\s*(.+)$', fm, re.MULTILINE)
                has_updated = re.search(r'^updated:', fm, re.MULTILINE)
                if has_date and not has_updated:
                    files.append((fp, has_date.group(1).strip()))

print(f'Found {len(files)} files to process')

for fp, date_str in sorted(files):
    date_str_clean = date_str.strip('"').strip("'")
    dt = None
    for fmt in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
        try:
            dt = datetime.strptime(date_str_clean, fmt)
            break
        except ValueError:
            continue
    if dt is None:
        print(f'SKIP (cannot parse date): {fp} -> {date_str}')
        continue

    updated_dt = dt + timedelta(days=1)

    with open(fp, 'r') as f:
        content = f.read()

    if 'T' in date_str and 'Z' in date_str:
        updated_str = updated_dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    elif ':' in date_str:
        updated_str = updated_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        updated_str = updated_dt.strftime('%Y-%m-%d')

    new_content = re.sub(
        r'^(date:\s*.+)$',
        r'\1\nupdated: ' + updated_str,
        content,
        count=1,
        flags=re.MULTILINE
    )

    with open(fp, 'w') as f:
        f.write(new_content)
    rel = os.path.relpath(fp, source_dir)
    print(f'OK: {rel} | date={date_str} -> updated={updated_str}')
