import AppKit
// usage: icon <glyph> <out.png> <px>
let a = CommandLine.arguments
let px = CGFloat(Double(a[3])!)
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(px), pixelsHigh: Int(px), bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
let s = NSAttributedString(string: a[1], attributes: [.font: NSFont(name: "STIXTwoMath-Regular", size: px * 0.9) ?? NSFont.systemFont(ofSize: px * 0.9), .foregroundColor: NSColor.white])
let r = s.boundingRect(with: NSSize(width: px * 2, height: px * 2), options: [.usesLineFragmentOrigin], context: nil)
s.draw(at: NSPoint(x: (px - r.width) / 2 - r.minX, y: (px - r.height) / 2 - r.minY))
NSGraphicsContext.restoreGraphicsState()
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
