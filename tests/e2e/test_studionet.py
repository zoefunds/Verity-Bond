"""Live, read-only E2E verification for the deployed Studionet contract."""

from hashlib import sha256
import os
from pathlib import Path
import subprocess

import pytest


RPC = "https://studio.genlayer.com/api"
ADDRESS = "0xe6859D98D3cD2532A76684454fF2edA809cd4834"
SOURCE_SHA256 = "8666fb1294c9bc106863b15788f94e81f0d12881852a704102d1c16fc4b7524d"
PACT_ID = "VB-LIVE-E2E-20261028-01"
ROOT = Path(__file__).parents[2]


pytestmark = [
    pytest.mark.studionet,
    pytest.mark.skipif(
        os.getenv("RUN_STUDIONET_E2E") != "1",
        reason="set RUN_STUDIONET_E2E=1 to query the live Studionet deployment",
    ),
]


def cli(*args: str) -> str:
    result = subprocess.run(
        ["genlayer", *args, "--rpc", RPC],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout + result.stderr


def test_deployed_source_matches_repository_contract():
    output = cli("code", ADDRESS)
    local = (ROOT / "contracts" / "VerityBond.py").read_text()
    # CLI progress messages may arrive on stderr after stdout when captured, so
    # assert the complete source as one intact payload instead of parsing a
    # stream-order-dependent footer.
    assert local.rstrip() in output
    assert sha256(local.encode()).hexdigest() == SOURCE_SHA256


def test_live_schema_exposes_the_complete_protocol_surface():
    output = cli("schema", ADDRESS)
    expected = {
        "begin_identity",
        "verify_identity",
        "open_pact",
        "submit_evidence_round",
        "challenge",
        "beneficiary_release",
        "finalize",
        "get_pact",
        "list_pacts",
        "pact_evidence",
        "get_ledger",
        "get_limits",
    }
    for method in expected:
        assert method in output
    assert "payable: true" in output
    assert "readonly: true" in output


def test_live_protocol_limits_match_the_reviewed_source():
    output = cli("call", ADDRESS, "get_limits")
    expected = {
        "breach_run": "2",
        "identity_ttl_seconds": "2592000",
        "max_body_chars": "180000",
        "max_coverage_gap_seconds": "604800",
        "max_indeterminate_rounds": "3",
        "min_release_rounds": "2",
        "review_window_seconds": "604800",
        "source_quorum": "2",
    }
    for key, value in expected.items():
        assert f"{key}: '{value}'" in output


def test_live_ledger_reflects_the_real_staked_pact_and_is_conserved():
    output = cli("call", ADDRESS, "get_ledger")
    fields = {}
    for key in ("currently_locked", "pacts", "total_in", "total_out"):
        marker = f"{key}: '"
        fields[key] = int(output.split(marker, 1)[1].split("'", 1)[0])
    assert fields["currently_locked"] == fields["total_in"] - fields["total_out"]
    assert fields == {
        "currently_locked": 1,
        "pacts": 1,
        "total_in": 1,
        "total_out": 0,
    }


def test_real_identity_bound_pact_is_persisted_on_chain():
    output = cli("call", ADDRESS, "get_pact", "--args", PACT_ID)
    expected = {
        "id": PACT_ID,
        "domain": "veritybond-live-e2e.vercel.app",
        "origin_url": "https://veritybond-live-e2e.vercel.app/commitment",
        "publisher": "0x7401c129EDfc26E68FE19309fE461eb3Db1058Eb",
        "beneficiary": "0xe2743b213418428A5BfBc7D9dDb8ec7c4c0D36De",
        "stake": "1",
        "state": "LIVE",
        "baseline_digest": "a4f65d22be3a7afe699a6e992b06fe5c106ebea4ba7250239aae32b9da168f2e",
        "statement_digest": "725d3c3bc90aa06f0b96ea77e24a8dd81827ce72752b9bdae78ddb6d0da15565",
    }
    for key, value in expected.items():
        assert f"{key}: '{value}'" in output
    assert "monitoring_rounds: '0'" in output
    assert "expires_at: '2026-11-11T09:03:42Z'" in output
    assert PACT_ID in cli("call", ADDRESS, "list_pacts")
