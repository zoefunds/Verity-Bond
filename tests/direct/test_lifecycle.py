import base64, gzip, hashlib, json, re
from urllib.parse import quote
ORIGIN="https://example.com/promise"
STATEMENT="This concrete public commitment remains in force for every customer."
def addrhex(value): return value.as_hex if hasattr(value,"as_hex") else "0x"+bytes(value).hex()
def warp(c,vm,when):
    vm.warp(when); c._now.__func__.__globals__["gl"].message_raw["datetime"]=when
def identity_and_open(c,vm,publisher,beneficiary,stake=100):
    vm.sender=publisher; warp(c,vm,"2026-10-28T12:00:00Z"); challenge=json.loads(c.begin_identity("example.com"))["challenge"]
    vm.mock_web("^"+re.escape("https://example.com/.well-known/veritybond.json")+"$",{"body":json.dumps({"wallet":addrhex(publisher),"challenge":challenge})}); c.verify_identity("example.com")
    vm.mock_web("^"+re.escape(ORIGIN)+"$",{"body":STATEMENT}); vm.mock_llm(".*",json.dumps({"verdict":"HOLDS","excerpt":""})); vm.value=stake
    c.open_pact("PACT-1","example.com",ORIGIN,STATEMENT,addrhex(beneficiary),30); vm.value=0
def evidence_round(c,vm,round_id,stamp,verdict):
    vm._llm_mocks.clear()
    wayback=f"https://web.archive.org/web/{stamp}id_/{ORIGIN}"; arquivo=f"https://arquivo.pt/wayback/{stamp}/{ORIGIN}"
    body=STATEMENT if verdict=="HOLDS" else "The commitment is withdrawn for every customer."; digest=hashlib.sha256(body.encode()).hexdigest()
    archive_digest=base64.b32encode(hashlib.sha1(body.encode()).digest()).decode().rstrip("=")
    vm.mock_web(re.escape("https://web.archive.org/cdx/search/cdx?")+".*"+stamp,{"body":json.dumps([["timestamp","original","statuscode","digest"],[stamp,ORIGIN,"200",archive_digest]])})
    vm.mock_web(re.escape("https://arquivo.pt/wayback/cdx?")+".*"+stamp,{"body":json.dumps({"url":ORIGIN,"timestamp":stamp,"status":"200","digest":"sha1:"+archive_digest})})
    vm.mock_web("^"+re.escape(wayback)+"$",{"body":body}); vm.mock_web("^"+re.escape(arquivo)+"$",{"body":body})
    vm.mock_llm(".*",json.dumps({"verdict":verdict,"excerpt":"The commitment is withdrawn" if verdict not in ("HOLDS","INDETERMINATE") else ""}))
    claims=[{"source":"WAYBACK","target_url":ORIGIN,"locator":wayback,"digest":digest},{"source":"ARQUIVO_PT","target_url":ORIGIN,"locator":arquivo,"digest":digest}]
    return c.submit_evidence_round("PACT-1",round_id,json.dumps(claims))
def capture_transfers(vm):
    transfers=[]
    def hook(_vm,request):
        if "PostMessage" in request: transfers.append(request["PostMessage"]); return {"ok":None}
    vm._gl_call_hook=hook; return transfers
def test_identity_baseline_evidence_and_expiry_release(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); identity_and_open(c,direct_vm,direct_alice,direct_bob)
    for i,stamp in enumerate(("20261029120000","20261105120000","20261112120000","20261119120000","20261126120000"),1): evidence_round(c,direct_vm,f"R{i}",stamp,"HOLDS")
    transfers=capture_transfers(direct_vm); warp(c,direct_vm,"2026-11-29T12:00:01Z"); c.finalize("PACT-1"); p=c.get_pact("PACT-1")
    assert p["state"]=="RELEASED" and p["returned"]=="100" and p["coverage_intact"] is True
    assert len(transfers)==1 and int(transfers[0]["value"])==100 and transfers[0]["address"].as_hex.lower()==addrhex(direct_alice).lower()
def test_indeterminate_resets_breach_and_expiry_refunds(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); identity_and_open(c,direct_vm,direct_alice,direct_bob); evidence_round(c,direct_vm,"R1","20261029120000","ABSENT"); evidence_round(c,direct_vm,"R2","20261030120000","INDETERMINATE")
    p=c.get_pact("PACT-1"); assert p["breach_run"]=="0" and p["last_verdict"]=="INDETERMINATE"
    transfers=capture_transfers(direct_vm); warp(c,direct_vm,"2026-11-29T12:00:01Z"); c.finalize("PACT-1"); assert c.get_pact("PACT-1")["state"]=="REFUNDED" and int(transfers[0]["value"])==100
def open_challenge(c,vm,publisher,beneficiary):
    identity_and_open(c,vm,publisher,beneficiary); evidence_round(c,vm,"B1","20261029120000","ABSENT"); evidence_round(c,vm,"B2","20261030120000","ABSENT"); assert c.get_pact("PACT-1")["state"]=="REVIEW"
    vm.sender=publisher; vm.value=10; c.challenge("PACT-1"); vm.value=0
def test_successful_challenge_returns_stake_and_bond(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); open_challenge(c,direct_vm,direct_alice,direct_bob); transfers=capture_transfers(direct_vm); evidence_round(c,direct_vm,"C1","20261031120000","HOLDS"); p=c.get_pact("PACT-1")
    assert p["state"]=="RELEASED" and p["returned"]=="110" and p["last_verdict"]=="HOLDS" and sum(int(x["value"]) for x in transfers)==110
def test_unresolved_challenge_pays_stake_and_returns_only_bond(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); open_challenge(c,direct_vm,direct_alice,direct_bob); transfers=capture_transfers(direct_vm)
    for i,stamp in enumerate(("20261031120000","20261101120000","20261102120000"),1): evidence_round(c,direct_vm,f"C{i}",stamp,"INDETERMINATE")
    p=c.get_pact("PACT-1"); assert p["state"]=="PAID" and p["paid"]=="100" and p["returned"]=="10"; assert [(x["address"].as_hex.lower(),int(x["value"])) for x in transfers]==[(addrhex(direct_bob).lower(),100),(addrhex(direct_alice).lower(),10)]
def test_metadata_timestamp_substitution_is_rejected(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); identity_and_open(c,direct_vm,direct_alice,direct_bob); stamp="20261029120000"; wayback=f"https://web.archive.org/web/{stamp}id_/{ORIGIN}"; arquivo=f"https://arquivo.pt/wayback/{stamp}/{ORIGIN}"
    direct_vm.mock_web("web.archive.org/cdx/search/cdx",{"body":json.dumps([["timestamp","original","statuscode","digest"],["20261029120001",ORIGIN,"200","x"]])})
    direct_vm.mock_web("arquivo.pt/wayback/cdx",{"body":json.dumps({"url":ORIGIN,"timestamp":stamp,"status":"200","digest":"x"})})
    claims=[{"source":"WAYBACK","target_url":ORIGIN,"locator":wayback,"digest":"x"},{"source":"ARQUIVO_PT","target_url":ORIGIN,"locator":arquivo,"digest":"x"}]
    with direct_vm.expect_revert("metadata"): c.submit_evidence_round("PACT-1","R1",json.dumps(claims))

def test_archive_index_digest_must_match_retrieved_payload(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); identity_and_open(c,direct_vm,direct_alice,direct_bob); stamp="20261029120000"
    body=STATEMENT; digest=hashlib.sha256(body.encode()).hexdigest(); wrong="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    wayback=f"https://web.archive.org/web/{stamp}id_/{ORIGIN}"; arquivo=f"https://arquivo.pt/wayback/{stamp}/{ORIGIN}"
    direct_vm.mock_web("web.archive.org/cdx/search/cdx",{"body":json.dumps([["timestamp","original","statuscode","digest"],[stamp,ORIGIN,"200",wrong]])})
    direct_vm.mock_web("arquivo.pt/wayback/cdx",{"body":json.dumps({"url":ORIGIN,"timestamp":stamp,"status":"200","digest":"sha1:"+wrong})})
    direct_vm.mock_web("^"+re.escape(wayback)+"$",{"body":body}); direct_vm.mock_web("^"+re.escape(arquivo)+"$",{"body":body})
    claims=[{"source":"WAYBACK","target_url":ORIGIN,"locator":wayback,"digest":digest},{"source":"ARQUIVO_PT","target_url":ORIGIN,"locator":arquivo,"digest":digest}]
    with direct_vm.expect_revert("archive index digest"): c.submit_evidence_round("PACT-1","R1",json.dumps(claims))

def test_archive_wire_digest_and_decoded_content_digest_are_separate(direct_deploy,direct_vm):
    c=direct_deploy("VerityBond.py"); url="https://archive.example/capture"
    wire=gzip.compress(STATEMENT.encode())
    direct_vm.mock_web("^"+re.escape(url)+"$",{"body":wire})
    fetched=c._fetch_text(url)
    assert fetched["ok"] is True and fetched["body"]==STATEMENT
    assert fetched["archive_digest"]==base64.b32encode(hashlib.sha1(wire).digest()).decode().rstrip("=")
    assert fetched["digest"]==hashlib.sha256(STATEMENT.encode()).hexdigest()

def test_capture_cannot_be_replayed_under_a_new_round_id(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); identity_and_open(c,direct_vm,direct_alice,direct_bob)
    evidence_round(c,direct_vm,"R1","20261029120000","HOLDS")
    with direct_vm.expect_revert("already been used"):
        evidence_round(c,direct_vm,"R2","20261029120000","HOLDS")

def test_review_deadline_pays_beneficiary(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); identity_and_open(c,direct_vm,direct_alice,direct_bob)
    evidence_round(c,direct_vm,"B1","20261029120000","ABSENT"); evidence_round(c,direct_vm,"B2","20261030120000","ABSENT")
    transfers=capture_transfers(direct_vm); warp(c,direct_vm,"2026-11-05T12:00:00Z"); c.finalize("PACT-1")
    assert c.get_pact("PACT-1")["paid"]=="100" and int(transfers[0]["value"])==100

def test_challenge_deadline_pays_stake_without_stranding_bond(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); open_challenge(c,direct_vm,direct_alice,direct_bob)
    transfers=capture_transfers(direct_vm); warp(c,direct_vm,"2026-11-05T12:00:00Z"); c.finalize("PACT-1")
    p=c.get_pact("PACT-1"); assert p["paid"]=="100" and p["returned"]=="10"
    assert sum(int(item["value"]) for item in transfers)==110

def test_only_beneficiary_can_release_a_positively_monitored_pact(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); identity_and_open(c,direct_vm,direct_alice,direct_bob)
    with direct_vm.expect_revert("beneficiary"): c.beneficiary_release("PACT-1")
    evidence_round(c,direct_vm,"R1","20261029120000","HOLDS")
    transfers=capture_transfers(direct_vm); direct_vm.sender=direct_bob; c.beneficiary_release("PACT-1")
    assert c.get_pact("PACT-1")["state"]=="RELEASED" and int(transfers[0]["value"])==100
    assert c.get_ledger()=={"total_in":"100","total_out":"100","currently_locked":"0","pacts":"1"}

def test_single_early_holds_or_coverage_gap_cannot_release(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); identity_and_open(c,direct_vm,direct_alice,direct_bob); evidence_round(c,direct_vm,"R1","20261029120000","HOLDS")
    warp(c,direct_vm,"2026-11-29T12:00:01Z"); c.finalize("PACT-1"); assert c.get_pact("PACT-1")["state"]=="REFUNDED"

def test_challenge_deadline_records_indeterminate_terminal_verdict(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); open_challenge(c,direct_vm,direct_alice,direct_bob)
    warp(c,direct_vm,"2026-11-05T12:00:00Z"); c.finalize("PACT-1")
    assert c.get_pact("PACT-1")["state"]=="PAID" and c.get_pact("PACT-1")["last_verdict"]=="INDETERMINATE"

def test_every_tested_terminal_path_conserves_total_value(direct_deploy,direct_vm,direct_alice,direct_bob):
    c=direct_deploy("VerityBond.py"); open_challenge(c,direct_vm,direct_alice,direct_bob)
    evidence_round(c,direct_vm,"C1","20261031120000","ABSENT")
    ledger=c.get_ledger(); assert ledger["total_in"]=="110" and ledger["total_out"]=="110" and ledger["currently_locked"]=="0"
