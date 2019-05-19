import frida

session = frida.attach("product_key_dork")

script = session.create_script("""
var base_addr = parseInt(Module.findBaseAddress('product_key_dork'),16);
var alpha = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_{}';
var f = new NativeFunction(ptr(base_addr + 0xb60), 'int', ['pointer', 'pointer']);

setTimeout(function () {
for (var i=0; i<alpha.length; i++) {
    for (var j=0; j<alpha.length; j++) {
        for (var k=0; k<alpha.length; k++) {
            for (var a=0; a<alpha.length; a++) {
                var attempt = "AAAAAAAAAA" + alpha.charAt(i) + alpha.charAt(j) + alpha.charAt(k) + alpha.charAt(a) + 'IIHU4AA3IQHBWTV514';
                //send(attempt)
                var x = Memory.allocUtf8String(attempt);
                var y = Memory.alloc(16);
                f(x,y)
                var out = new Uint8Array(Memory.readByteArray(y, 20));
                if (out['19'] == 48 && out['18'] == 242 && out['17'] == 251 && out['16'] == 119 && out['15'] == 111 && out['14'] == 110 && out['13'] == 101 && out['12'] == 107 && out['11'] == 97 && out['10'] == 105 && out['9'] == 107 && out['8'] == 97 && out['7'] == 115 && out['6'] == 105) {
                    send('Found: ' + attempt, out)
                }
                //send('bytes', out)
                }
            }
        }
    }
    send('done')
    }, 0);

    //send('array', new Uint8Array(Memory.readByteArray(y, 16)));
""")

script.on('message', on_message)
script.load()


