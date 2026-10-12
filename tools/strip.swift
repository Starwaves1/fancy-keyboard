import AppKit
let a = CommandLine.arguments
let lines = a[1].components(separatedBy: "|")
let w = 1400, h = 70 * lines.count
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
NSColor.white.setFill(); NSRect(x: 0, y: 0, width: w, height: h).fill()
for (i, l) in lines.enumerated() {
  NSAttributedString(string: l, attributes: [.font: NSFont.systemFont(ofSize: 40)]).draw(at: NSPoint(x: 10, y: h - 70 * (i + 1) + 10))
}
NSGraphicsContext.restoreGraphicsState()
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
