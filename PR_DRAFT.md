# l10n(fr): Add French UI translation

Adds a French (`fr`) ARB localization, translating all UI strings in
`app_en.arb` (910 keys) into French.

Relates to #901 (multi-language support / translator onboarding).

## What this changes
- `lib/l10n/app_fr.arb` (new): French translations for every key present
  in `app_en.arb`, with identical structure — same key set, ICU
  placeholders, plural/select rules, and `@metadata` blocks untouched.
- `lib/l10n/app_en.arb`, `app_es.arb`, `app_de.arb`: add a `french`
  language-name string (mirrors how `german` was added next to
  `spanish`).
- `lib/constants/types/type_constants.dart`: add `LocaleConstants.french`.
- `lib/providers/locale_provider.dart`: mention French alongside
  Spanish/German in the "force English until backend is ready" comments
  and the language-name switch. **French is not added to the supported
  / selectable locales** — same gated state as Spanish and German today.

## Scope
UI strings only — no app/content/audio changes. Register is formal
("vous"), matching the tone used by the major French meditation apps on
the stores (Petit BamBou, Headspace, Calm, Insight Timer, Waking Up all
vouvoie their users). Verbs, imperatives, and possessives (ton/ta/tes →
votre/vos, toi → vous) were adjusted accordingly, not just swapped
mechanically — each changed string was reread for correct agreement and
elision (e.g. "tu t'es" → "vous vous êtes", "Appuie" → "Appuyez").

## Not included
`app_localizations_fr.dart` (generated output) isn't committed — I
don't have Flutter available locally to run `flutter gen-l10n`. Happy
to run it and push the generated file once CI confirms the ARB is
good, or if a maintainer prefers to generate it on merge.

The local ARB-validation helper script I used while translating is not
part of this PR, to keep the diff focused on the translation itself.

## Follow-up
I'm a native French speaker and happy to keep this translation updated
as new strings are added to `app_en.arb` — just tag me on new copy.
