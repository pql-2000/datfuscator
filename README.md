# Experimental algebraic- and data-oriented obfuscation

Datfuscator is a work-in-progress obfuscator for all kinds of data and computations.

Its main goal is to provide an abstract interface to describe algebraic computations, and to provide functionality to rewrite said computations in such a way that they are equivalent, but more complex to understand. This can be helpful for naive DRM implementations, writing capture-the-flag challenges, and various other goals.

Take for example the very simple algebraic expression

```
a = x + y
``` 

In the python language, this can be rewritten as:

```python
a=0;c=0;l1=x;l2=y;r=0xFFFF-l1>>31&0x10;l1>>=r;w=0xFF-l1>>31&0x8;l1>>=w;r|=w;w=0xF-l1>>31&0x4;l1>>=w;r|=w;w=0x3-l1>>31&0x2;l1>>=w;r|=w;r|=(l1>>1);l1=r;r=0xFFFF-l2>>31&0x10;l2>>=r;w=0xFF-l2>>31&0x8;l2>>=w;r|=w;w=0xF-l2>>31&0x4;l2>>=w;r|=w;w=0x3-l2>>31&0x2;l2>>=w;r|=w;r|=(l2>>1);l2=r
for i in range(max(l2+1,l1+1)+1):
    x1=int(x&(1<<i)!=0);y1=int(y&(1<<i)!=0);z=0;z2=x1+y1+c;z=int(z2>=2);c=z;a^=(-(z2%2)^a)&(1<<i)
```

Which is a non-trivial equivalent expression. (with all applicable advantages and disadvantages).

Likewise, the string:

```python
"hello\n"
```

can be rewritten as an array of XOR products:

```python
''.join([chr((ord(__ll1l) ^ ord(__lll1))) for (__ll1l, __lll1) in zip('£lWþÓ©', 'Ë\t;\x92¼£')])
```

Whilst these examples show conversion to python-compatible code, this project aims to provide an abstracted interface which is able to target many different programming languages.


## Disclaimer

```
Usage of datfuscator for malicious intent is not endorsed by the developers in any way, shape, or form. It is the end user's responsibility to obey all applicable local, state and
federal laws. Developers assume no liability and are not responsible for any misuse or
damage caused by this software
```