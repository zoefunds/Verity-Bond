def test_veritybond_deploys_with_empty_conserved_ledger(direct_deploy):
    contract = direct_deploy("VerityBond.py")
    assert contract.list_pacts() == []
    assert contract.get_ledger() == {
        "total_in": "0", "total_out": "0", "currently_locked": "0", "pacts": "0"
    }
    limits = contract.get_limits()
    assert limits["source_quorum"] == "2"
    assert limits["max_indeterminate_rounds"] == "3"
    assert limits["max_coverage_gap_seconds"] == "604800"
    assert limits["min_release_rounds"] == "2"

def test_identity_challenge_is_domain_scoped(direct_deploy):
    contract = direct_deploy("VerityBond.py")
    result = contract.begin_identity("Example.COM")
    assert '"domain": "example.com"' in result
    assert '"path": "/.well-known/veritybond.json"' in result

def test_unverified_publisher_cannot_open_pact(direct_deploy, direct_vm):
    contract = direct_deploy("VerityBond.py")
    with direct_vm.expect_revert("identity"):
        contract.open_pact("VB-1", "example.com", "https://example.com/promise",
                           "This concrete public commitment remains in force for all users.",
                           "0x1111111111111111111111111111111111111111", 30)

def test_breach_excerpt_must_exist_in_admitted_body(direct_deploy, direct_vm):
    contract = direct_deploy("VerityBond.py")
    with direct_vm.expect_revert("not present"):
        contract._validated_finding({"verdict": "ABSENT", "excerpt": "invented text"},
                                    "The admitted page contains different words.")

def test_grounded_breach_finding_is_accepted(direct_deploy):
    contract = direct_deploy("VerityBond.py")
    assert contract._validated_finding(
        {"verdict": "WEAKENED", "excerpt": "only where practical"},
        "The service now applies only where practical for operators.",
    ) == ("WEAKENED", "only where practical")
