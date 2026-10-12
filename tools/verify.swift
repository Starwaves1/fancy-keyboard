import Carbon
import Foundation
// Registers + enables the layouts, then types "nothing. sorry to bother." through each via UCKeyTranslate.
let dir = URL(fileURLWithPath: NSHomeDirectory() + "/Library/Keyboard Layouts")
print("register:", TISRegisterInputSource(dir as CFURL))
let codes: [UInt16] = [45,31,17,4,34,45,5,47,49,1,31,15,15,16,49,17,31,49,11,31,17,4,14,15,47]
let shiftCodes: [UInt16] = [45,31]
let list = TISCreateInputSourceList(nil, true).takeRetainedValue() as! [TISInputSource]
for src in list {
  let id = Unmanaged<CFString>.fromOpaque(TISGetInputSourceProperty(src, kTISPropertyInputSourceID)).takeUnretainedValue() as String
  guard id.hasPrefix("org.unknown.keylayout.") else { continue }
  TISEnableInputSource(src)
  guard let p = TISGetInputSourceProperty(src, kTISPropertyUnicodeKeyLayoutData) else { print(id, "NO LAYOUT DATA"); continue }
  let data = Unmanaged<CFData>.fromOpaque(p).takeUnretainedValue() as Data
  func type(_ cs: [UInt16], _ mod: UInt32) -> String {
    data.withUnsafeBytes { raw -> String in
      let lay = raw.baseAddress!.assumingMemoryBound(to: UCKeyboardLayout.self)
      var s = ""
      for c in cs {
        var dead: UInt32 = 0; var len = 0; var buf = [UniChar](repeating: 0, count: 8)
        UCKeyTranslate(lay, c, UInt16(kUCKeyActionDown), mod, UInt32(LMGetKbdType()), 0, &dead, 8, &len, &buf)
        s += String(utf16CodeUnits: buf, count: len)
      }
      return s
    }
  }
  print(id, "|", type(codes, 0) + type([18], 2), "| shift:", type(shiftCodes, 2), "| cmd:", type([8], 1), "| opt:", type([8,27], 8) + type([27], 10), "| digits:", type([18,19], 0))
}
