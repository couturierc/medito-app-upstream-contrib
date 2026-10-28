#!/usr/bin/env python3
"""Validate app_fr.arb against app_en.arb: JSON validity, key set, and ICU placeholders."""
import json
import re
import sys

PLACEHOLDER_RE = re.compile(r'\{([a-zA-Z0-9_]+)\s*(?:,|\})')

def placeholders(value):
    if not isinstance(value, str):
        return set()
    return set(PLACEHOLDER_RE.findall(value))

def main():
    en = json.load(open('lib/l10n/app_en.arb', encoding='utf-8'))
    fr = json.load(open('lib/l10n/app_fr.arb', encoding='utf-8'))

    en_keys = {k for k in en if not k.startswith('@')}
    fr_keys = {k for k in fr if not k.startswith('@')}

    errors = []

    missing = en_keys - fr_keys
    extra = fr_keys - en_keys
    if missing:
        errors.append(f"Missing {len(missing)} keys in app_fr.arb: {sorted(missing)[:10]}")
    if extra:
        errors.append(f"Extra {len(extra)} keys in app_fr.arb: {sorted(extra)[:10]}")

    if fr.get('@@locale') != 'fr':
        errors.append(f"@@locale is {fr.get('@@locale')!r}, expected 'fr'")

    mismatches = []
    for k in sorted(en_keys & fr_keys):
        en_ph = placeholders(en[k])
        fr_ph = placeholders(fr[k])
        if en_ph != fr_ph:
            mismatches.append((k, sorted(en_ph), sorted(fr_ph)))
    if mismatches:
        errors.append(f"Placeholder mismatch in {len(mismatches)} keys:")
        for k, e, f in mismatches[:20]:
            errors.append(f"  {k}: en={e} fr={f}")

    # ICU plural/select sanity: count of 'other{' occurrences should match
    plural_mismatches = []
    for k in sorted(en_keys & fr_keys):
        en_v, fr_v = en[k], fr[k]
        if isinstance(en_v, str) and 'plural' in en_v:
            en_other = en_v.count('other{')
            fr_other = fr_v.count('other{') if isinstance(fr_v, str) else 0
            if en_other != fr_other or 'plural' not in (fr_v or ''):
                plural_mismatches.append(k)
    if plural_mismatches:
        errors.append(f"Plural structure mismatch: {plural_mismatches}")

    print(f"en keys: {len(en_keys)}  fr keys: {len(fr_keys)}")
    print(f"Keys match: {not missing and not extra}")
    print(f"Placeholders identical for all shared keys: {not mismatches}")
    print(f"Plural structures preserved: {not plural_mismatches}")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print("\nAll checks passed.")

if __name__ == '__main__':
    main()
