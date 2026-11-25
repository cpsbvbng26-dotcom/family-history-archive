#!/usr/bin/env python3
"""The checks of family-history-archive.

  python3 verification/check.py            offline: the index against the quotations kept in verification/sources.json
  python3 verification/check.py --online   fetch every location and every source again from main of its repository
  python3 verification/check.py --break    every check fails when the thing it watches is broken (offline)

The index lists where transcriptions of primary sources about the operator's deceased ancestors already are. It copies
no transcription. A person enters only when a public record of the operator calls that person deceased and states the
relation (DECEASED below, after verification/kinship.js of cpsbvbng26-dotcom). A name that the operator's records
withhold is withheld here too, and this file keeps it only as a SHA-256 value.
"""
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rules  # noqa: E402
from rules import add, jload, sub  # noqa: E402

PROSE = ["README.md", "README.en.md"]
IDX = "data/index.json"
SRC = "verification/sources.json"
FIELDS = {"id", "person", "primary_source", "jacar", "transcription_ja", "transcription_en", "location", "doi", "rights_ja",
          "rights_en", "repository", "commit", "read", "sources"}
UA = {"User-Agent": "family-history-archive-check/1.0 (+https://github.com/cpsbvbng26-dotcom/family-history-archive)"}
SELF = {"verification/check.py", "verification/rules.py"}

# People whom a public record of the operator calls deceased, with the words of relation that may stand next to the name,
# and the kept quotations that state the death and the relation. The words are let through only in a file that also holds
# the name (a word without the name might be about someone else), as in verification/kinship.js of cpsbvbng26-dotcom.
DECEASED = [
    {"name": "大谷恒", "words": ["外曾祖父", "外曽祖父", "曾祖父", "great-grandfather"],
     "death": "ngn-deceased", "relation": "ngn-relation", "relation_word": "外曾祖父"},
]

# Names that the operator's records withhold, kept only as the SHA-256 of the NFKC, case-folded name. The name is not
# written in this repository in any form. cpsbvbng26-dotcom's docs/external-evaluations.md withholds one name because it is
# not known whether the person is alive (self-correction SC-023); this index keeps that decision.
WITHHELD = {3: {"227add3db6a712b65b6bc48bd46f922f838a4b7804493ce0a0552b45b19b79fb"}}
MARK = "〔氏名を伏せた一名〕"

# The words of rule 10 of cpsbvbng26-dotcom (verification/kinship.js, the Japanese and English parts): a word that points to
# one relative, and sentences that attribute thoughts or plans to the parents or describe the family's religion.
JO = "(?:が|の|は|を|も|に|と|へ|から)"
OVER = re.compile("|".join([
    "(?<![祖曾曽伯叔義分])(?:父|母)" + JO + "|父親|母親",
    r"(?:外)?(?:曾|曽|高)?祖(?:父|母)|(?:伯|叔)(?:父|母)|義(?:父|母|兄|姉|弟|妹)",
    "(?<![師子門姉兄])(?:兄|姉|弟|妹)" + JO,
    r"(?:私|わたし|著者|筆者|運営者)の(?:配偶者|妻|夫)",
    r"\b(?:my|the author['’]s|the operator['’]s) (?:father|mother|grandfather|grandmother|great-grandfather|great-grandmother|brother|sister|uncle|aunt|spouse|wife|husband|father-in-law|mother-in-law|brother-in-law|sister-in-law)\b",
]), re.I)
ATTRIB = re.compile("|".join([
    r"両親(?:の|が|は|も|から|に|とも)[^。\n]*?(?:理解|了解|了承|承諾|同意|賛成|反対|許し|許可|希望|意向|意見|考え|計画|予定|気持ち|思い|願い|望み|期待|心配|喜|応援|支持|納得|認め|望ん|願っ|思っ|知っ|祝福)",
    r"\bparents\b[^.\n]*?\b(?:understand|understood|know|knew|agree|approve|consent|support|accept|wish|hope|want|plan|feel|felt|think|thought|believe|bless)\w*",
    r"家の(?:伝統|宗旨|宗教|宗派|祭祀|祖霊|しきたり|習わし|菩提寺)|(?:家|一族|実家)(?:の|が)?(?:宗旨|宗派|檀家|氏子)",
    r"\b(?:family|household)(?:['’]s)? (?:tradition|religion|faith|rite|rites|denomination|shrine|temple)\b",
]), re.I)


def index(F):
    return (jload(F, IDX) or {}).get("entries", [])


def S(F):
    return jload(F, SRC) or {}


def quote(F, k):
    return S(F).get("quotes", {}).get(k, {}).get("text", "")


def today():
    return datetime.date.today().isoformat()


def table_rows(text, head):
    i = text.find("\n" + head + "\n")
    if i < 0:
        return None
    rows = []
    for line in text[i + 1:].split("\n")[2:]:
        if not line.startswith("|"):
            break
        rows.append([c.strip() for c in line.strip().strip("|").split(" | ")])
    return rows


def section(text, head):
    i = text.find("\n" + head + "\n")
    if i < 0:
        return ""
    j = text.find("\n## ", i + len(head) + 2)
    return text[i:j if j >= 0 else len(text)]


def let_through(text):
    """Take out the words of relation of a deceased person, in a file that holds the person's name."""
    for p in DECEASED:
        if p["name"] in text:
            for w in p["words"]:
                text = text.replace(w, "〓")
    return text


# ------------------------------------------------------------------ the index

def schema(F):
    bad = []
    E = index(F)
    Q = S(F).get("quotes", {})
    N = jload(F, "verification/numbers.json") or {}
    if not E:
        return ["the index cannot be read"]
    if [e.get("id") for e in E] != ["F%d" % n for n in range(1, len(E) + 1)]:
        bad.append("entries are not numbered F1, F2, ... in order")
    names = {p["name"] for p in DECEASED}
    for e in E:
        i = e.get("id", "?")
        if set(e) != FIELDS:
            bad.append("%s: the fields (%s)" % (i, ", ".join(sorted(set(e) ^ FIELDS))))
            continue
        if e["person"] not in names:
            bad.append(i + ": a person whom no public record calls deceased")
        if e["primary_source"] != quote(F, "ngn-citation") or "Ref." + e["jacar"] not in e["primary_source"]:
            bad.append(i + ": the citation is not the form the record where it is kept prescribes")
        m = re.fullmatch(r"https://github\.com/(cpsbvbng26-dotcom/[\w.-]+)/blob/main/(\S+)", e["location"])
        if not m or m.group(1) != e["repository"]:
            bad.append(i + ": the location is not a file on main of the operator's repository")
        if e["commit"] != S(F).get("commits", {}).get(e["repository"]):
            bad.append(i + ": the commit is not the one the sources were read at")
        if e["read"] > today() or e["read"] not in N.get("dates", {}) or e["read"] != S(F).get("read"):
            bad.append(i + ": the date read")
        if not e["sources"] or any(s not in Q for s in e["sources"]):
            bad.append(i + ": a source that is not a kept quotation")
        if e["doi"] is not None and ("DOI [%s]" % e["doi"]) not in quote(F, "ngn-doi"):
            bad.append(i + ": a DOI that the record where it is kept does not write")
        lic = "CC BY 4.0" if "[CC BY 4.0](LICENSE)" in quote(F, "ngn-licence") else None
        if not lic or not e["rights_ja"].startswith(lic + "。") or not e["rights_en"].startswith(lic + ". "):
            bad.append(i + ": the rights do not start with the licence of the record where it is kept")
        if "原資料の画像は、どこにも置いていません。" not in e["rights_ja"] or "No image of the original is kept anywhere." not in e["rights_en"]:
            bad.append(i + ": the rights do not say that no image of the original is kept")
    return bad


def deceased(F):
    """Every person of the index is called deceased, and the relation is stated, in the kept quotations."""
    bad = []
    for p in DECEASED:
        d, r = quote(F, p["death"]), quote(F, p["relation"])
        if p["name"] not in d or not re.search("戦死|死去|故人|亡くな", d):
            bad.append(p["name"] + ": no kept quotation calls the person deceased")
        if p["name"] not in r or p["relation_word"] not in r:
            bad.append(p["name"] + ": no kept quotation states the relation")
    for f, head, n in (("README.md", "| 人物 | 続柄 | 故人であることと続柄の出どころ |", 0),
                       ("README.en.md", "| Person | Relation | Where the death and the relation are stated |", 1)):
        rows = table_rows(F.get(f, ""), head)
        got = [(row[0], row[1]) for row in rows or []]
        want = [(p["name"], p["relation_word"] if n == 0 else "great-grandfather (%s)" % p["relation_word"]) for p in DECEASED]
        if got != want:
            bad.append(f + ": the table of persons is not the list of the deceased")
    return bad


def readme_tables(F):
    bad = []
    for f, head, n in (("README.md", "| 番号 | 人物 | 史料 | 翻刻 | 所在 | 権利 | 読んだ日 |", 0),
                       ("README.en.md", "| No. | Person | Source | Transcription | Location | Rights | Read |", 1)):
        rows = table_rows(F.get(f, ""), head)
        if rows is None or len(rows) != len(index(F)):
            bad.append(f + ": the table of the index is not data/index.json")
            continue
        for row, e in zip(rows, index(F)):
            want = [e["id"], e["person"], e["primary_source"], e["transcription_" + ("ja" if n == 0 else "en")]]
            if row[:4] != want or "](%s)" % e["location"] not in row[4] or row[5] != e["rights_" + ("ja" if n == 0 else "en")] or row[6] != e["read"]:
                bad.append(f + ": the row %s differs from data/index.json" % e["id"])
            if (e["doi"] and "](https://doi.org/%s)" % e["doi"] not in row[4]) or (not e["doi"] and "doi.org" in row[4]):
                bad.append(f + ": the DOI of %s" % e["id"])
    return bad


def withheld(F):
    """No withheld name in any file, in any width or case; the place where the hiding is told keeps the mark and the reason."""
    bad = []
    test = F.get("__test_hashes__") or {}
    for f, t in F.items():
        if f.startswith("__"):
            continue
        n = rules.norm(t)
        for L in set(WITHHELD) | set(test):
            hs = WITHHELD.get(L, set()) | test.get(L, set())
            for i in range(len(n) - L + 1):
                if hashlib.sha256(n[i:i + L].encode("utf-8")).hexdigest() in hs:
                    bad.append(f + ": a withheld name")
                    break
    ja, en = F.get("README.md", ""), F.get("README.en.md", "")
    if MARK not in ja or MARK not in en or MARK not in quote(F, "hub-withheld-mark"):
        bad.append("the READMEs do not keep the mark of the withheld name")
    if "伏せた理由は、存命かどうかを確かめていないことです。" not in ja or "because it is not known whether that person is alive" not in en \
            or "存命かどうかを確かめていない人物です。" not in quote(F, "hub-withheld") or "SC-023" not in quote(F, "sc-023"):
        bad.append("the reason for withholding the name is not told, or not in the kept quotations")
    if "伏せた決めは、そのまま保ちます。" not in ja or "keeps the decision to withhold it as it is" not in en:
        bad.append("the READMEs do not say that the decision is kept")
    return bad


IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".tif", ".tiff", ".webp", ".bmp", ".pdf", ".svg")
REGISTER_LINES = {".zenodo.json": ["no family register"],
                  "README.md": ["- 戸籍と除籍の記載の中身、その画像と転写、本籍は置きません。"],
                  "README.en.md": ["- No content, image or transcription of a family register (戸籍 or 除籍), and no registered domicile (本籍), is kept."]}


def images_and_registers(F, paths=None):
    """No image or PDF in the repository (no JACAR image, rule 11 of cpsbvbng26-dotcom); no link to an image viewer; the words
    for a family register and a registered domicile only in the sentence that says none is kept."""
    bad = []
    for p in (paths if paths is not None else all_paths()):
        if p.lower().endswith(IMAGE_EXT):
            bad.append(p + ": an image or a PDF")
    copies = set((jload(F, "verification/copies.json") or {}).get("copies", {}))
    for f, t in F.items():
        if f in SELF or f == "CLAUDE.md" or f in copies or f.startswith(".github/") or f.startswith("__"):
            continue
        if re.search(r"jacar\.archives\.go\.jp/(?:das/image|aj/meta/imageen|das/viewer)|\.(?:png|jpe?g|tiff?)\b", t, re.I):
            bad.append(f + ": a link to an image")
        rest = t
        for s in REGISTER_LINES.get(f, []):
            rest = rest.replace(s, "")
        rest = rest.replace("戸籍と除籍の", "") if f == "CLAUDE.md" else rest
        if re.search("戸籍|除籍|本籍|謄本|抄本|family register|domicile", rest, re.I):
            bad.append(f + ": a family register outside the sentence that says none is kept")
    for f, lines in ((k, v) for k, v in REGISTER_LINES.items() if k in PROSE):
        if any(s not in F.get(f, "") for s in lines):
            bad.append(f + ": the sentence that keeps no family register")
    if "JACAR の原資料の画像は置きません。" not in F.get("README.md", "") or "No image of an original at JACAR is kept." not in F.get("README.en.md", ""):
        bad.append("the READMEs do not say that no JACAR image is kept")
    return bad


def all_paths():
    out = []
    for dp, dns, fns in os.walk(rules.ROOT):
        dns[:] = [d for d in dns if d not in rules.SKIP_DIRS]
        out += [os.path.relpath(os.path.join(dp, fn), rules.ROOT).replace(os.sep, "/") for fn in fns]
    return out


def kinship(F):
    """Rule 10: no word that points to a single relative, except the words of a deceased person next to the name; no
    sentence that gives the parents thoughts or plans or describes the family's religion. The base words of rules.py too."""
    bad = []
    for f, t in F.items():
        if f in SELF or f == "CLAUDE.md":
            continue
        m = OVER.search(let_through(t))
        if m:
            bad.append(f + ": a word for one relative「" + m.group(0) + "」")
        m = ATTRIB.search(t)
        if m:
            bad.append(f + ": a sentence about the parents or the family「" + m.group(0)[:30] + "」")
    G = {f: let_through(t) for f, t in F.items() if f not in SELF}
    return bad + rules.words_not_written(G)


REMOVED = {"README.md": ["かつて cpsbvbng26-dotcom に、先祖の公的記録の頁がありました。",
                         "その頁は、2026-09-11 に運営者の指示で消されました。self-correction の SC-032 が、そのことを記録しています。",
                         "この索引は、その頁の中身を戻しません。"],
           "README.en.md": ["cpsbvbng26-dotcom once had a page of public records of ancestors.",
                            "The page was removed on 2026-09-11 at the operator's instruction, as SC-032 of self-correction records.",
                            "This index does not restore what that page held."]}


def removed_page(F):
    """The page of ancestors removed on 2026-09-11 is not restored: the READMEs say so, the kept quotation records the
    removal, and nothing links to the removed page or to the history that holds it."""
    bad = []
    for f, must in REMOVED.items():
        for s in must:
            if s not in F.get(f, ""):
                bad.append(f + ": lacks「" + s[:24] + "」")
    if "利用者の指示で四つの頁を消しました。" not in quote(F, "sc-032"):
        bad.append("the kept quotation of SC-032")
    for f, t in F.items():
        if f in SELF:
            continue
        if re.search(r"lineage(?:\.en)?\.html|cpsbvbng26-dotcom/(?:blob|tree|commit)/(?!main/)[0-9a-f]{7,40}", t):
            bad.append(f + ": a link to the removed page or to the history that holds it")
    return bad


COI = {"README.md": ["運営者は、この索引が挙げる人物の子孫です。", "この索引は、史料の読みを足しません。",
                     "史料が述べることと、家に伝わることを、同じ項目に混ぜません。"],
       "README.en.md": ["The operator is a descendant of the person this index names.", "This index adds no reading of the sources.",
                        "What the sources say and what the family hands down are not mixed in one entry."]}


def conflict(F):
    """The note on the conflict of interest comes first and says the operator is a descendant; the motive of kinship is in
    the kept quotation."""
    bad = []
    for f, head in (("README.md", "## 利益相反"), ("README.en.md", "## Conflict of interest")):
        t = F.get(f, "")
        sec = section(t, head)
        if not sec or t.find("\n" + head + "\n") > t.find("\n## ", t.find("\n## ") + 1) or t.find("\n" + head + "\n") != t.find("\n## "):
            bad.append(f + ": the note on the conflict of interest is not the first section")
        for s in COI[f]:
            if s not in sec:
                bad.append(f + ": the note on the conflict of interest lacks「" + s[:24] + "」")
    if "動機は血縁" not in quote(F, "ngn-motive"):
        bad.append("the kept quotation of the motive")
    return bad


COUNTERS = {"entries": lambda F: len(index(F))}

CHECKS = [
    ("The index: fields, the deceased, the citation, the location on main, the commit, the date, the DOI, the rights", schema),
    ("Every person is called deceased, and the relation stated, in the kept quotations; both READMEs list them", deceased),
    ("Both READMEs carry the index word for word", readme_tables),
    ("No withheld name in any file; the mark and the reason are kept", withheld),
    ("No image or PDF, no link to an image, and no family register outside the sentence that keeps none", lambda F: images_and_registers(F)),
    ("Rule 10: no word for one relative but the deceased's next to the name, nothing on the parents or the family's religion", kinship),
    ("The removed page of ancestors is not restored, and nothing links to it", removed_page),
    ("The conflict of interest comes first: the operator is a descendant", conflict),
    ("Copies of the canonical files and the licences are byte-identical (sha256)", rules.copies),
    ("No subject that these repositories do not write about", rules.topics_not_written),
    ("No list of work for the operator", rules.no_tasks),
    ("No e-mail address in any file", rules.no_email),
    ("Workflows: actions pinned to commits, permissions, timeouts; Dependabot", rules.workflows),
    ("labels.yml makes the labels of the canonical workflows", lambda F: rules.labels(F)),
    ("CLAUDE.md carries rules 16, 17 and 18 (10 times)", rules.claude_md),
    ("The writing rules: です/ます, no second person, no bold, one dash per paragraph, short sentences", lambda F: rules.prose(F, PROSE)),
    ("Every number in prose is in the ledger of numbers, and every count matches the index", lambda F: rules.numbers(F, PROSE, COUNTERS, PROSE)),
    ("README.md and README.en.md link each other, disclose the language model and name the licences", rules.readme_pair),
    (".zenodo.json: one creator with the ORCID iD, the licence of LICENSE, the disclosure, the licence sentence, related identifiers found in the repository", rules.zenodo),
]


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def online(F):
    bad, cache = [], {}
    for k, q in S(F)["quotes"].items():
        key = (q["repository"], q["file"])
        if key not in cache:
            try:
                cache[key] = fetch("https://raw.githubusercontent.com/%s/main/%s" % key).decode("utf-8")
            except Exception as e:
                cache[key] = None
                bad.append("%s %s could not be fetched: %s" % (key[0], key[1], e))
        if cache[key] is not None and q["text"] not in cache[key]:
            bad.append("%s: the quotation %s is no longer in %s on main" % (key[0], k, key[1]))
    for e in index(F):
        m = re.fullmatch(r"https://github\.com/(cpsbvbng26-dotcom/[\w.-]+)/blob/main/(\S+)", e["location"])
        try:
            if not m or not fetch("https://raw.githubusercontent.com/%s/main/%s" % (m.group(1), m.group(2))):
                bad.append(e["id"] + ": the location is empty")
        except Exception as x:
            bad.append("%s: the location could not be fetched: %s" % (e["id"], x))
    for b in bad:
        print("  FAIL  " + b)
    print("\nonline: %d files, %d quotations, %d locations, %d problems." % (len(cache), len(S(F)["quotes"]), len(index(F)), len(bad)))
    return 1 if bad else 0


def _test_name(G):
    """The withheld name is not known to this file. The break adds the hash of a test word to the list and writes the word."""
    w = "テスト用の名"
    G["__test_hashes__"] = {len(w): {hashlib.sha256(rules.norm(w).encode("utf-8")).hexdigest()}}
    G["README.md"] = G["README.md"] + "\n" + w + "\n"


def _test_name_wide(G):
    w = "ＴＥＳＴＮＡＭＥ"
    G["__test_hashes__"] = {len("testname"): {hashlib.sha256("testname".encode("utf-8")).hexdigest()}}
    G["data/index.json"] = G["data/index.json"] + w


C = [c[0] for c in CHECKS]
BREAKS = [
    (C[0], "a person whom no public record calls deceased", sub(IDX, '"id": "F2",\n      "person": "大谷恒"', '"id": "F2",\n      "person": "大谷某"')),
    (C[0], "an unknown field", sub(IDX, '"id": "F1",', '"id": "F1",\n      "rank": "x",')),
    (C[0], "a location off main", sub(IDX, "naval-gazette-notes/blob/main/data/", "naval-gazette-notes/blob/30ac46e6871f23110daeec98d254530fe737430e/data/")),
    (C[0], "a DOI that the record does not write", sub(IDX, '"doi": "10.5281/zenodo.22055709"', '"doi": "10.5281/zenodo.22055708"')),
    (C[0], "a date read in the future", lambda G: G.__setitem__(IDX, G[IDX].replace('"read": "2026-11-25"', '"read": "2099-01-01"', 1))),
    (C[0], "rights that leave out the image", sub(IDX, '原資料の画像は、どこにも置いていません。"', '"')),
    (C[0], "a citation in another form", sub(IDX, '"primary_source": "JACAR（アジア歴史資料センター）Ref.C12070491000、', '"primary_source": "JACAR Ref.C12070491000、')),
    (C[1], "the kept quotation no longer calls the person deceased", sub(SRC, "そのうち大谷恒は戦死しています。", "そのうち大谷恒は存命です。")),
    (C[1], "the kept quotation no longer states the relation", sub(SRC, "報道の大谷恒（著者の外曾祖父）と同一人物です。", "報道の大谷恒と同一人物です。")),
    (C[1], "README.en.md gives another relation", sub("README.en.md", "| 大谷恒 | great-grandfather (外曾祖父) |", "| 大谷恒 | grandfather |")),
    (C[2], "README.md drops the DOI", sub("README.md", "（DOI [10.5281/zenodo.22055709](https://doi.org/10.5281/zenodo.22055709)）", "")),
    (C[2], "README.en.md gives another date read", sub("README.en.md", "No image of the original is kept anywhere. | 2026-11-25 |", "No image of the original is kept anywhere. | 2026-11-24 |")),
    (C[2], "README.md points F2 elsewhere", sub("README.md", "(https://github.com/cpsbvbng26-dotcom/naval-gazette-notes/blob/main/data/investiture-1943-09-11.csv)", "(https://github.com/cpsbvbng26-dotcom/naval-gazette-notes/blob/main/data/README.md)")),
    (C[3], "a listed name in a README (a test word stands in for the name)", _test_name),
    (C[3], "a listed name in full-width letters (a test word stands in for the name)", _test_name_wide),
    (C[3], "README.md drops the mark", sub("README.md", "〔氏名を伏せた一名〕がいます。", "氏名を伏せた人がいます。")),
    (C[3], "README.en.md drops the reason", sub("README.en.md", "because it is not known whether that person is alive", "for privacy")),
    (C[4], "a family register in the README", add("README.md", "\n戸籍の記載では、名は一字違います。\n")),
    (C[4], "a link to a JACAR image", add("README.en.md", "\nhttps://www.jacar.archives.go.jp/das/image/C12070491000\n")),
    (C[4], "an image in the repository", lambda G: G.__setitem__("__paths__", ["data/gazette.png"])),
    (C[4], "README.en.md drops that no JACAR image is kept", sub("README.en.md", "No image of an original at JACAR is kept.", "Images may follow.")),
    (C[5], "a word for one relative without the name", add("README.en.md", "\nThe operator's grandfather kept the medals.\n")),
    (C[5], "a living relative's word in Japanese", add("README.md", "\n著者の祖母が語りました。\n")),
    (C[5], "the family's religion", add("README.md", "\n家の宗旨は記録していません。\n")),
    (C[5], "another ancestor's relation word, for whom no record states a death", add("data/index.json", " 高" + "祖父")),
    (C[6], "README.md restores the removed page", sub("README.md", "- この索引は、その頁の中身を戻しません。\n", "")),
    (C[6], "a link to the removed page", add("README.en.md", "\nhttps://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/d6549f6^/lineage.html\n")),
    (C[7], "README.md drops that the operator is a descendant", sub("README.md", "運営者は、この索引が挙げる人物の子孫です。\n", "")),
    (C[7], "the note on the conflict of interest moves after the index", lambda G: G.__setitem__("README.en.md", G["README.en.md"].replace("## Conflict of interest\n", "## Conflict\n", 1).replace("## Index\n", "## Conflict of interest\n", 1).replace("## Conflict\n", "## Index\n", 1))),
    (C[8], "one character of SECURITY.md", sub("SECURITY.md", "7 日以内", "8 日以内")),
    (C[9], "a word for a political organisation", add("README.md", "\n" + rules.dec("5pS/5YWa") + "\n")),
    (C[10], "a list of work for the operator", add("README.md", "\n戸籍の写しは" + "運営者が確かめる。\n")),
    (C[11], "an e-mail address", add("README.en.md", "\nwriter" + "@" + "example.com\n")),
    (C[12], "an action named by its version", sub(".github/workflows/check.yml", "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1", "actions/checkout@v7")),
    (C[13], "labels.yml drops a label", sub(".github/workflows/labels.yml", 'gh label create "erratum"', 'gh label create "error"')),
    (C[14], "CLAUDE.md loses rule 18", sub("CLAUDE.md", "**合っているかを、最低 10 回確かめる。**", "**合っているかを確かめる。**")),
    (C[15], "a sentence not in です/ます", add("README.md", "\n索引は所在だけを持つ。\n")),
    (C[16], "a count that differs from the index", sub("README.md", "項目は 2 件です。", "項目は 3 件です。")),
    (C[16], "a number not in the ledger of numbers", add("README.en.md", "\nThe list has 10 names.\n")),
    (C[17], "README.en.md does not link the Japanese page", sub("README.en.md", "[日本語](./README.md)", "日本語")),
    (C[18], ".zenodo.json gives an affiliation", sub(".zenodo.json", '"orcid": "0009-0000-1406-0547"', '"orcid": "0009-0000-1406-0547", "affiliation": "x"')),
    (C[18], ".zenodo.json names a related identifier found nowhere else", sub(".zenodo.json", '"identifier": "10.5281/zenodo.22055709"', '"identifier": "10.5281/zenodo.' + "9" * 8 + '"')),
]


if __name__ == "__main__":
    F = rules.load()
    if "--online" in sys.argv:
        sys.exit(online(F))
    if "--break" in sys.argv:
        # The image break hands its own list of paths to the check, since the map of files holds text only.
        def wrapped(G):
            paths = G.pop("__paths__", None)
            return images_and_registers(G, paths if paths is not None else all_paths())
        CHECKS[4] = (C[4], wrapped)
    sys.exit(rules.run(CHECKS, BREAKS, F, sys.argv))
