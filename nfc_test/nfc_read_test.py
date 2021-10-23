import binascii
import nfc


def main():
  clf = nfc.ContactlessFrontend('usb')
  # 212F(FeliCa)
  target_suica = nfc.clf.RemoteTarget("212F")
  # 0003(Suica)
  target_suica.sensf_req = bytearray.fromhex("0000030000")

  # 212F(FeliCa) 学生証用に2つ起動させておく(suica以外のカード)
  target_req = nfc.clf.RemoteTarget("212F")


  target = None
  while True:
    target_res = clf.sense(target_suica, iterations=10, interval=0.01)
    target_res2 = clf.sense(target_req, iterations=10, interval=0.01)
    if target_res is not None:
        target = target_res
        break
    elif target_res2 is not None:
        target = target_res2
    if target is not None:
        tag = nfc.tag.activate(clf,target)
        tag.sys = 3
        idm = binascii.hexlify(tag.idm)
        print(idm)
        break
  clf.close()


if __name__ == '__main__':
    main()


