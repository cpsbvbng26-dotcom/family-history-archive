# family-history-archive

[日本語](./README.md)

An index of where, in the operator's repositories, transcriptions of primary sources about deceased ancestors of the operator are kept.
The index holds only the location, the source, the rights and the date read.
The transcriptions themselves are not copied here.
Each entry points to the place where the material already is.
The index was set down on 2026-11-20.

The archive is on Zenodo. The DOI of the first version is [`10.5281/zenodo.24397144`](https://doi.org/10.5281/zenodo.24397144), and the DOI common to all versions is [`10.5281/zenodo.24397143`](https://doi.org/10.5281/zenodo.24397143).

## Conflict of interest

The operator is a descendant of the person this index names.
The README of naval-gazette-notes calls Otani Tsune (大谷恒) the author's great-grandfather (外曾祖父).
N5 in the errata of the same repository says that the motive for studying this source was kinship.
When a descendant lists the sources about an ancestor, what is chosen and how it is read can lean towards the ancestor.
This index adds no reading of the sources.
Readings, and what can and cannot be established, follow the record where each source is kept.
What the sources say and what the family hands down are not mixed in one entry.

## Index

There are 2 entries.
Every entry points to a location on main of one of the operator's repositories.

| No. | Person | Source | Transcription | Location | Rights | Read |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | 大谷恒 | JACAR（アジア歴史資料センター）Ref.C12070491000、海軍公報（部内限）號外　昭和十八年九月十一日發令（防衛省防衛研究所） | The transcription in section 3 of the source note (the frozen PDF) | [pdf/naval-gazette-entry-otani-tsune.pdf in naval-gazette-notes](https://github.com/cpsbvbng26-dotcom/naval-gazette-notes/blob/main/pdf/naval-gazette-entry-otani-tsune.pdf) (DOI [10.5281/zenodo.22055709](https://doi.org/10.5281/zenodo.22055709)) | CC BY 4.0. How the gazette itself is treated is not decided in naval-gazette-notes. No image of the original is kept anywhere. | 2026-11-20 |
| F2 | 大谷恒 | JACAR（アジア歴史資料センター）Ref.C12070491000、海軍公報（部内限）號外　昭和十八年九月十一日發令（防衛省防衛研究所） | The same transcription in machine-readable form (CSV and JSON) | [data/investiture-1943-09-11.csv in naval-gazette-notes](https://github.com/cpsbvbng26-dotcom/naval-gazette-notes/blob/main/data/investiture-1943-09-11.csv) | CC BY 4.0. How the gazette itself is treated is not decided in naval-gazette-notes. No image of the original is kept anywhere. | 2026-11-20 |

| Person | Relation | Where the death and the relation are stated |
| --- | --- | --- |
| 大谷恒 | great-grandfather (外曾祖父) | The sections 「扱う人」 and 「史料の外にあるもの」 of the README of naval-gazette-notes |

The source is cited in the form the record where it is kept prescribes, in Japanese.
The DOI is copied from the README of naval-gazette-notes, which says the versions were checked against DataCite on 2026-11-11.
The work on this index did not consult DataCite.

## Not entered

- cpsbvbng26-dotcom once had a page of public records of ancestors.
- The page was removed on 2026-09-11 at the operator's instruction, as SC-032 of self-correction records.
- This index does not restore what that page held.
- The person that page named besides Otani Tsune has no transcription of a primary source in public now, so the index does not enter that person.
- The record of external evaluations of cpsbvbng26-dotcom has one person whose name is withheld (〔氏名を伏せた一名〕).
- The name was withheld because it is not known whether that person is alive, as SC-023 of self-correction records.
- This index does not write that name either, and keeps the decision to withhold it as it is.
- No content, image or transcription of a family register (戸籍 or 除籍), and no registered domicile (本籍), is kept.
- No image of an original at JACAR is kept. Under rule 11 of cpsbvbng26-dotcom, the Center for Military History of the National Institute for Defense Studies is to be contacted first.
- The section 「史料の外にあるもの」 of the README of naval-gazette-notes holds news reports, inquiries, what is handed down in the family, and objects once kept by relatives. These are not transcriptions of primary sources, so they are not entered.
- The other recipients on the same list are not ancestors, so they are not named here.

## Fields of an entry

| Field | Content |
| --- | --- |
| `id` | The number, starting with F |
| `person` | The person: only someone whom a public record calls deceased and whose relation it states |
| `primary_source` | The citation of the primary source, in the form the record where it is kept prescribes |
| `jacar` | The JACAR reference code |
| `transcription_ja`・`transcription_en` | What the transcription is |
| `location` | Where the transcription already is |
| `doi` | The DOI written by the record where it is kept, or `null` |
| `rights_ja`・`rights_en` | The rights: the licence of that record and how the original is treated |
| `repository`・`commit` | The repository of the location, and its commit on main when it was read |
| `read` | The date read |
| `sources` | The names of quotations in `verification/sources.json` |

## Checks

```
python3 verification/check.py            # fields, quotations, the deceased and the relation, withheld names, images and registers, kinship words, disclosure, copies, writing, numbers
python3 verification/check.py --online   # fetch the locations and the sources again from main, and see that they exist and still hold the quotations
python3 verification/check.py --break    # break each check once and see it fail
```

The withheld name is kept in the checks only as a SHA-256 value, not as the name.
The breaking check therefore adds a test word in place of the name and sees the same mechanism fail.

CI runs the offline check and the breaking check on every push and pull request.
The online check runs as a separate job at the same times and once a week.

## Operator

The operator is Takuya Nemoto (根本卓哉).
ORCID iD: [0009-0000-1406-0547](https://orcid.org/0009-0000-1406-0547).
Errors are received through the [error report](https://github.com/cpsbvbng26-dotcom/family-history-archive/issues/new?template=error-report.yml) form.
Security issues are received by the route in [SECURITY.md](./SECURITY.md).
Requests about a person in the sources the index points to are received where the source is kept.
The README of naval-gazette-notes names the section "Statements about people" of the [Disclaimer](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/DISCLAIMER.en.md) of cpsbvbng26-dotcom for that.

## Use of language models

The use of language models is set out in the same table as in the other repositories.

| Tool | Used for | Checked by |
| --- | --- | --- |
| Claude Code (Anthropic) | The entries of the index, README text, the checks in `verification/`, and the quotations from the records where the sources are kept | The checks of `verification/check.py`; there is no record of the operator reading and checking it |

Claude Code wrote the entries after reading those records on 2026-11-20.
The sources themselves were not read again.
Claude is not an author.

## Licence

The index and the text are [CC BY 4.0](./LICENSE); the code is [MIT](./LICENSE-CODE).
The rights in the transcriptions and data where they are kept follow the licence of each location.
