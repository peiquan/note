# sun.misc.unsafe

原文翻译自:http://mishadoff.com/blog/java-magic-part-4-sun-dot-misc-dot-unsafe/

unsafe 是学习 Java 并发必须了解一个基础类，其源码可以查看[sun.misc.Unsafe][],类的介绍如下：
```
A collection of methods for performing low-level, unsafe operations.
Although the class and all methods are public, use of this class is
limited because only trusted code can obtain instances of it.
```

这个类提供了低级别、不安全操作的集合。尽管类的方法都是 public 的，不过我们其使用还是受限的，因为只有可信任的代码（比如 jdk 源码）才可以随意使用。

受限使用，表明我们不能轻易地获取到 Unsafe 对象的使用，比如说 :
```
Unsafe unsafe = new Unsafe();
```
因为 Unsafe 的构造方法是私有的，所以这种方法行不通；或者像 java.util.concurrent.atomic.AtomicInteger 等方法一样:
```
static {
    try {
        valueOffset = unsafe.objectFieldOffset
            (AtomicInteger.class.getDeclaredField("value"));
    } catch (Exception ex) { throw new Error(ex); }
}
```
这种操作在 jdk 源码中可以，不过在我们写的代码中是不可以的，因为我们的代码是不被信任的。

查看源码，我们发现在 Unsafe 中有一个静态属性 theUnsafe ，这时，我们可以通过反射获取其使用权，代码如下:
```
Field f = Unsafe.class.getDeclaredField("theUnsafe");
f.setAccessible(true);
Unsafe unsafe = (Unsafe) f.get(null);
```

## Unsafe 介绍
Unsafe 里有上百个方法，大致可以分为以下几类:

### Info 
获取底层内存的信息

- addressSize
- pageSize


### Objects 
Provides methods for object and its fields manipulation.

- allocateInstance
- objectFieldOffset


## Classes
Provides methods for classes and static fields manipulation.

- staticFieldOffset
- defineClass
- defineAnonymousClass
- ensureClassInitialized


## Arrays
Arrays manipulation.

- arrayBaseOffset
- arrayIndexScale

### Synchronization
Low level primitives for synchronization.

-monitorEnter
-tryMonitorEnter
-monitorExit
-compareAndSwapInt
-putOrderedInt

### Memory
Direct memory access methods.

-allocateMemory
-copyMemory
-freeMemory
-getAddress
-getInt
-putInt


## Unsafe 的使用点
### 另类的初始化
假设一个类如下:
```
class A {
    private long a; 

    public A() {
        this.a = 1; 
    }

    public long a() { return this.a; }
}
```
使用构造函数，反射和 Unsafe 得到不同的初始化结果:
```
A o1 = new A();
System.out.println(o1.a());// 1

A o2 = A.class.newInstance();
System.out.println(o2.a());// 1

A o3 = (A)unsafe.allocateInstance(A.class);
System.out.println(o3.a());// 0

```











[sun.misc.Unsafe]:http://www.docjar.com/html/api/sun/misc/Unsafe.java.html
