from .. import ops
from .. import storage
from .. import api as weave
from .. import artifacts_local
from .. import weave_internal


def test_autocommit(cereal_csv):
    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "C"  # value before set is 'C'

    weave.use(ops.set(weave_internal.const(csv[-1]["type"]), "XXXX"))

    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "XXXX"

    weave.use(ops.set(weave_internal.const(csv[-1]["type"]), "YY"))

    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "YY"


def test_nonconst(cereal_csv):
    # note, not doing a use here.
    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "C"  # value before set is 'C'
    weave.use(ops.set(weave_internal.const(csv[-1]["type"]), "XXXX"))
    # cache.RESULT_CACHE.clear()
    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "XXXX"
    weave.use(ops.set(weave_internal.const(csv[-1]["type"]), "YY"))
    # cache.RESULT_CACHE.clear()
    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "YY"


def test_mutate_with_use(cereal_csv):
    csv = ops.local_path(cereal_csv).readcsv()
    weave.use(ops.set(weave_internal.const(csv[-1]["type"]), "XXXX"))
    assert weave.use(csv[-1]["type"]) == "XXXX"
    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "XXXX"


def test_mutate_artifact():
    storage.save({"a": 5, "b": 6}, "my-dict")
    dict_obj = ops.get(
        f"local-artifact://{artifacts_local.local_artifact_dir()}/my-dict/latest"
    )
    weave.use(ops.set(weave_internal.const(dict_obj["a"]), 17))
    assert weave.use(dict_obj["a"]) == 17


def test_csv_saveload_type(cereal_csv):
    csv = weave.use(ops.local_path(cereal_csv).readcsv())
    ref = storage.save(csv)
    storage.get(str(ref))


def test_skips_list_indexcheckpoint(cereal_csv):
    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "C"  # value before set is 'C'

    row = ops.List.__getitem__(ops.list_indexCheckpoint(csv), -1)
    weave.use(ops.set(weave_internal.const(row["type"]), "XXXX"))

    csv = ops.local_path(cereal_csv).readcsv()
    assert weave.use(csv[-1]["type"]) == "XXXX"