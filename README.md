# Local-Bardode
Addon for Blender that allows the creation of various barcode types

![Cover Image](readme_images/cover.jpg)

This addon allows you to create various barcodes as meshes. It currently supports QR, MicroQR, PDF417, and Aztec codes.

This addon started life as the [Local QR Code](https://github.com/welshjf/blender-local-qrcode) addon by Jacob Welsh. I [previously](https://blenderartists.org/t/local-qrcode-addon-updated/1150498) updated it to work with blender 2.8, and have since greatly expanded it. Since it now supports more than just QR codes, I have renamed it to Local Barcodes.

This is my first real addon, and my first foray into BPY and python beyond just updating old addons. The code is probably messy, and I'm sure there will be bugs. Let me know if you run into any problems.

These currently only work in Object Mode. They might half work in edit mode, but if they do, it's unintended.

# Summary of the barcodes:
<details>
  <summary>QR Codes</summary>

![qr_light](readme_images/qr_light.jpg) ![qr_dark](readme_images/qr_dark.jpg)

QR codes are most commonly used for marketing. They are also sometimes used in electronics or manufacturing as machine readable product numbers. They will often contain a URL, although they can hold any text or numbers. They can hold many common symbols. Technically, they can hold kanji as well, but I could not get it working. If you can get Blender to take kanji as a text input, it *should* automatically switch to kanji encoding mode. If it doesn't, please let me know.

QR codes can have error correction. This means they can still be read after being damaged, at the cost of a larger code. Higher EC level, bigger code, more damage tolerance, up to 30%. 
At max size, and with lowest EC level, they can theoretically store up to 4,296 alphanumeric characters. Bear in mind that large codes are VERY hard to scan with phone cameras.
</details>

<details>
  <summary>MicroQR</summary>

![micro_light](readme_images/micro_light.jpg) ![micro_dark](readme_images/micro_dark.jpg) 


MicroQR codes are smaller versions of QR codes. They have a higher information density, but a much smaller top size. Big warning: they are VERY rare, and I do not believe a single Android app can read them. Apparently, the [i-nigma](https://apps.apple.com/us/app/i-nigma-qr-code-data-matrix-and-1d-barcode-reader/id388923203) app for apple devices can read them, but I can't test this. If you find an Android app that can scan these, let me know.
</details>



<details>
  <summary>Aztec Codes</summary>

![aztec_light](readme_images/aztec_light.jpg) ![aztec_dark](readme_images/aztec_dark.jpg)

Aztec codes are commonly used on boarding passes, and medical labeling and equipment. They can be read inverted and mirrored and require no quiet space around them. They are less common than QR codes, and the scanner app support for them is a little rarer and less reliable. They have error Correction support, but I could not figure out how to control this in the generator library. I believe the generated codes have some, but I do not know how much.
</details>


<details>
  <summary>PDF417 Codes</summary>


![pdf_light](readme_images/pdf_light.jpg) ![pdf_dark](readme_images/pdf_dark.jpg)

PDF417 codes are commonly used for logistics, document management, and ID cards and systems. If you have a US Drivers license, there is probably one on it. They can have a very high data density. PDF417s can theoretically hold up to 1850 alphanumeric characters, but in practice, due to encoding differences, it will be lower. They support multiple levels of Error Correction. These are more difficult than the others here to read with a cellphone camera, so if that is the goal, try to keep it fairly small.
</details>

While this addon does not yet support 1D barcodes, I can recommend the [3 of 9](https://www.fontspace.com/i-shot-the-serif/free-3-of-9) font. It is a code 39 barcode. If using it, remember to start and end the text with * symbols, as they are used as beginning and end markers.

I personally use these barcodes with [Decal Machine](https://blenderartists.org/t/decalmachine/688181) to turn them into decals, but as they are meshes, you can do whatever you want with them. 

The reasoning behind the "Local" in the title is that this addon uses no online services to generate barcodes. It generates them entirely locally using a few different open source libraries. 
The libraries used and liscenses are:

* [Segno](https://github.com/heuer/segno) - BSD
* [pdf417-py](https://github.com/ihabunek/pdf417-py), also called [pdf417gen](https://pypi.org/project/pdf417gen/0.2.0/) - MIT
* [aztec_code_generator](https://github.com/delimitry/aztec_code_generator) - MIT


The most reliable Android apps I have found for scanning the less common barcode types are [Scan Them All - 2D & Barcodes](https://play.google.com/store/apps/details?id=gr.webq.codescanner&hl=en_US) and [Neo Reader](https://play.google.com/store/apps/details?id=de.gavitec.android).

Future plans:
* Datamatrix codes
* 1D codes
* any other 2D barcodes. If you can find a pure python library that generates a 2D barcode that I don't have here, I will happily give them a look over to see if I can implement it.
