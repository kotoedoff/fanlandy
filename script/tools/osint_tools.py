import subprocess
import sys
from pathlib import Path

def run_maigret(username, timeout=30):
    maigret_path = Path(__file__).parent.parent.parent / "soft" / "maigret"
    if not maigret_path.exists():
        return {"error": "Maigret not installed"}
    try:
        result = subprocess.run([sys.executable, "-m", "maigret", username, "--timeout", str(timeout)], capture_output=True, text=True, cwd=str(maigret_path))
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def run_holehe(email):
    holehe_path = Path(__file__).parent.parent.parent / "soft" / "holehe"
    if not holehe_path.exists():
        return {"error": "Holehe not installed"}
    try:
        result = subprocess.run([sys.executable, "-m", "holehe", email], capture_output=True, text=True, cwd=str(holehe_path))
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def run_toutatis(username):
    toutatis_path = Path(__file__).parent.parent.parent / "soft" / "toutatis"
    if not toutatis_path.exists():
        return {"error": "Toutatis not installed"}
    try:
        result = subprocess.run([sys.executable, "toutatis.py", username], capture_output=True, text=True, cwd=str(toutatis_path))
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def run_sherlock(username):
    try:
        result = subprocess.run(["sherlock", username], capture_output=True, text=True, timeout=60)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "Sherlock not installed. Install: pip install sherlock-project"}
    except Exception as e:
        return {"error": str(e)}

def run_blackbird(username):
    try:
        result = subprocess.run(["blackbird", "--username", username], capture_output=True, text=True, timeout=60)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "Blackbird not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_ghunt(email):
    try:
        result = subprocess.run(["ghunt", "email", email], capture_output=True, text=True, timeout=60)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "GHunt not installed. Install: pip install ghunt"}
    except Exception as e:
        return {"error": str(e)}

def run_phoneinfoga(phone):
    try:
        result = subprocess.run(["phoneinfoga", "scan", "-n", phone], capture_output=True, text=True, timeout=60)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "PhoneInfoga not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_spiderfoot(target):
    try:
        result = subprocess.run(["spiderfoot", "-s", target], capture_output=True, text=True, timeout=120)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "SpiderFoot not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_theharvester(domain):
    try:
        result = subprocess.run(["theHarvester", "-d", domain, "-b", "all"], capture_output=True, text=True, timeout=120)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "theHarvester not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_whatsmyname(username):
    try:
        result = subprocess.run(["whatsmyname", "-u", username], capture_output=True, text=True, timeout=60)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "WhatsMyName not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_socialscan(query):
    try:
        result = subprocess.run(["socialscan", query], capture_output=True, text=True, timeout=60)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "SocialScan not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_spiderfoot(target):
    try:
        result = subprocess.run(["spiderfoot", "-s", target], capture_output=True, text=True, timeout=120)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "SpiderFoot not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_theharvester(domain):
    try:
        result = subprocess.run(["theHarvester", "-d", domain, "-b", "all"], capture_output=True, text=True, timeout=120)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "theHarvester not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_reconng(domain):
    try:
        result = subprocess.run(["recon-ng", "-m", "recon/domains-hosts/hackertarget", "-o", f"SOURCE={domain}"], capture_output=True, text=True, timeout=120)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "Recon-ng not installed"}
    except Exception as e:
        return {"error": str(e)}

def run_webcheck(url):
    try:
        result = subprocess.run(["web-check", url], capture_output=True, text=True, timeout=60)
        return {"status": "success", "output": result.stdout, "error": result.stderr}
    except FileNotFoundError:
        return {"error": "Web-check not installed"}
    except Exception as e:
        return {"error": str(e)}
