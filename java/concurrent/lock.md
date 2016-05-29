# 锁
参考资料:

- [自旋锁、排队自旋锁、MCS锁、CLH锁](http://coderbee.net/index.php/concurrent/20131115/577/comment-page-1)
- [http://www.tuicool.com/articles/2INzUb](http://www.tuicool.com/articles/2INzUb)

互斥锁，自旋锁，排队自旋锁，CLH 锁，MCS 锁

## 互斥锁与自旋锁的区别
### 原理

互斥锁是指当一个线程尝试获取某个锁时，如果该锁已被其他线程占用，该线程挂起或睡眠。

自旋锁是指当一个线程尝试获取某个锁时，如果该锁已被其他线程占用，就一直循环检测锁是否被释放。

## 使用场景

互斥锁适用于临界区持锁时间比较长的操作，比如下面这些情况都可以考虑

- 临界区有IO操作
- 临界区代码复杂或者循环量大
- 临界区竞争非常激烈
- 单核处理器

自旋锁适用于临界区持锁时间非常短且CPU资源不紧张的情况下。

互斥锁的起始开销高于自旋锁，且有上下文切换，不过倒属于一劳永逸的方案，临界区的持锁时间不过对互斥锁的开销造成影响。自旋锁是死循环检测，起始开销比互斥锁小，且没有上下文切换，但随着持锁时间增加，其开销会线性增加。

## 互斥锁
典型的互斥锁就是 synchronized 关键字的使用.

## 自旋锁
### 简易的实现
原子更新某个变量即可，这个变量可以是一个引用，也可以是一个标识位。原子更新就是借助 cas 循环检查。下面给出两种几乎一样的实现：
```
public class SpinLock {

    private volatile AtomicBoolean isLock = new AtomicBoolean();

    public void lock() {
        while (!isLock.compareAndSet(false,true)) {
        }
    }

    public void unlock() {
        isLock.compareAndSet(true,false);
    }
}
```

```
public class SpinLock {

    private AtomicReference<Thread> owner = new AtomicReference<Thread>();

    public void lock() {
        Thread currentThread = Thread.currentThread();
        while (!owner.compareAndSet(null, currentThread)) {
        }
    }

    public void unlock() {
        Thread currentThread = Thread.currentThread();
        owner.compareAndSet(currentThread, null);
    }
}
```

测试代码
```
final SpinLock lock = new SpinLock();
lock.lock();
for (int i = 0; i < 10; i++) {
    new Thread(new Runnable() {

        public void run() {
            lock.lock();
            System.out.println(Thread.currentThread().getId() + " execute");
            lock.unlock();
        }
    }).start();
    Thread.sleep(100);
}
System.out.println("main thread unlock!");
lock.unlock();
```

