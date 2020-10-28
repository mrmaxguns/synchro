from diff_match_patch import diff_match_patch

dmp = diff_match_patch()


def diff(doc1, doc2):
    patches = dmp.patch_make(doc1, doc2)
    return dmp.patch_toText(patches)


def patch(diff, doc):
    patches = dmp.patch_fromText(diff)
    new_text, _ = dmp.patch_apply(patches, doc)
    return new_text
