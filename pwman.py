#!/usr/bin/env python3
"""
密管 pwman —— 命令行密码管理器

  pip install cryptography
  python pwman.py init          # 初始化保险库
  python pwman.py add           # 添加一条密码
  python pwman.py list          # 列出所有标题
  python pwman.py get github    # 查看某条（含密码）
  python pwman.py search mail   # 搜索
  python pwman.py gen 20        # 生成 20 位随机密码
  python pwman.py del github    # 删除

保险库 ~/.pwman/vault.dat 由主密码经 PBKDF2 派生密钥后 Fernet 加密。
"""
import os, sys, json, base64, getpass, secrets, string

VAULT = os.path.expanduser("~/.pwman/vault.dat")

def _crypto():
    try:
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        from cryptography.fernet import Fernet, InvalidToken
        return PBKDF2HMAC, hashes, Fernet, InvalidToken
    except ImportError:
        sys.exit("请先安装: pip install cryptography")

def _key(password: str, salt: bytes) -> bytes:
    PBKDF2HMAC, hashes, Fernet, _ = _crypto()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=salt, iterations=200_000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def _load_entries(password):
    _, _, Fernet, InvalidToken = _crypto()
    with open(VAULT, "rb") as f:
        salt, token = f.read().split(b"\n", 1)
    salt = base64.b64decode(salt)
    try:
        raw = Fernet(_key(password, salt)).decrypt(token)
    except InvalidToken:
        sys.exit("❌ 主密码错误")
    return json.loads(raw), salt

def _save_entries(password, entries, salt):
    _, _, Fernet, _ = _crypto()
    token = Fernet(_key(password, salt)).encrypt(json.dumps(entries).encode())
    os.makedirs(os.path.dirname(VAULT), exist_ok=True)
    with open(VAULT, "wb") as f:
        f.write(base64.b64encode(salt) + b"\n" + token)
    os.chmod(VAULT, 0o600)

def cmd_init():
    if os.path.exists(VAULT):
        sys.exit("保险库已存在")
    pw = getpass.getpass("设置主密码: ")
    if pw != getpass.getpass("再输一次: "):
        sys.exit("两次不一致")
    _save_entries(pw, [], secrets.token_bytes(16))
    print("✅ 保险库已创建:", VAULT)

def cmd_add():
    pw = getpass.getpass("主密码: ")
    entries, salt = _load_entries(pw)
    title = input("标题: ").strip()
    if not title: sys.exit("标题不能为空")
    entries.append({
        "title": title,
        "user": input("用户名: ").strip(),
        "pass": getpass.getpass("密码 (留空自动生成): ") or gen_password(16),
        "url": input("网址: ").strip(),
        "note": input("备注: ").strip(),
    })
    _save_entries(pw, entries, salt)
    print("✅ 已保存")

def cmd_list():
    pw = getpass.getpass("主密码: ")
    entries, _ = _load_entries(pw)
    for i, e in enumerate(entries, 1):
        print(f"{i}. {e['title']}  {e['user']}")

def cmd_get(keyword):
    pw = getpass.getpass("主密码: ")
    entries, _ = _load_entries(pw)
    hit = [e for e in entries if keyword.lower() in e["title"].lower()]
    if not hit: sys.exit("没找到")
    e = hit[0]
    print(f"标题: {e['title']}\n用户: {e['user']}\n密码: {e['pass']}\n网址: {e['url']}\n备注: {e['note']}")

def cmd_search(keyword):
    pw = getpass.getpass("主密码: ")
    entries, _ = _load_entries(pw)
    for e in entries:
        if keyword.lower() in (e["title"] + e["user"] + e["url"]).lower():
            print(f"- {e['title']}  {e['user']}")

def cmd_del(keyword):
    pw = getpass.getpass("主密码: ")
    entries, salt = _load_entries(pw)
    hit = [e for e in entries if keyword.lower() in e["title"].lower()]
    if not hit: sys.exit("没找到")
    e = hit[0]
    if input(f"删除「{e['title']}」? [y/N] ").lower() != "y": sys.exit("取消")
    entries.remove(e)
    _save_entries(pw, entries, salt)
    print("🗑️ 已删除")

def gen_password(n=16):
    cs = string.ascii_letters + string.digits + "!@#$%^&*-_=+"
    return "".join(secrets.choice(cs) for _ in range(n))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    {"init": cmd_init, "add": cmd_add, "list": cmd_list,
     "search": lambda: cmd_search(sys.argv[2]),
     "get": lambda: cmd_get(sys.argv[2]),
     "del": lambda: cmd_del(sys.argv[2]),
     "gen": lambda: print(gen_password(int(sys.argv[2]) if len(sys.argv) > 2 else 16)),
     }.get(cmd, lambda: sys.exit(__doc__))()
