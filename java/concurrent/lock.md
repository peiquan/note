# 锁
参考资料:

- [自旋锁、排队自旋锁、MCS锁、CLH锁](http://coderbee.net/index.php/concurrent/20131115/577/comment-page-1)
- [Java并发包源码学习之AQS框架（二）CLH lock queue和自旋锁](http://www.tuicool.com/articles/2INzUb)

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

### 公平性的实现
自旋锁虽然简易，不过却不公平，有可能最早申请锁的线程最晚才获取到，这是不理想。假设我们虽然保证公平性，即 FIFO，那我们就需要保存申请锁的顺序。而这种顺序性，自然就是通过线性链表来实现。如下:

```
public class CLHLock {
    public static class CLHNode {
        private Thread thread;
        private volatile boolean isLocked = true; // 默认是在等待锁
        public CLHNode(Thread thread) {
            this.thread = thread;
        }

        public Thread getThread() {
            return thread;
        }

        public boolean isLocked() {
            return isLocked;
        }

        public void setLocked(boolean locked) {
            isLocked = locked;
        }
    }

    private volatile CLHNode tail ;
    private static final AtomicReferenceFieldUpdater<CLHLock, CLHNode> UPDATER = AtomicReferenceFieldUpdater
            . newUpdater(CLHLock.class, CLHNode .class , "tail" );

    public void lock(CLHNode currentThread) {
        CLHNode preNode = UPDATER.getAndSet( this, currentThread);
        if(preNode != null) { //已有线程占用了锁，进入自旋
            while(preNode.isLocked) {
            }
        }
    }

    public void unlock(CLHNode currentThread) {
        currentThread.setLocked(false);// 改变状态，让后续线程结束自旋
    }
}
```

公平性我们倒是实现了，却发现，CLHLock 有很多自旋其实都没有必要，比如下面的测试代码:
```
 final CLHLock lock = new CLHLock();
CLHNode mainNode = new CLHNode(Thread.currentThread());
lock.lock(mainNode);

for (int i = 0; i < 10; i++) {
    new Thread(new Runnable() {
        public void run() {
            CLHNode tempNode = new CLHNode(Thread.currentThread());
            lock.lock(tempNode);
            System.out.println(Thread.currentThread().getId() + " execute");
            lock.unlock(tempNode);
        }
    }).start();
    Thread.sleep(10);
}

lock.unlock(mainNode);
System.out.println("main thread unlock! " + mainNode.isLocked);
```

在 mainNode 没有释放锁之前，其余 10 个线程一直在自旋，其实这样做很没有必要，因为按照公平性而言，只有第一个线程的自旋是有用的，而其他线程的自旋，会徒增 cpu 的负担，甚至直达 100%。那么有没有办法减少这种自旋呢 ？ 最简单的方法，就是每一次自旋之间加入一个休眠，如下:
```
if(preNode != null) { //已有线程占用了锁，进入自旋
    while(preNode.isLocked) {
    	Thread.currentThread().sleep(30);
    }
}
```

cpu 降下来了，却发现因为休眠的关系，导致了线程执行的延迟，这也是不太友好的，那有没有办法只让即将执行的线程在自旋，其他线程都在等待。答案肯定是有的。从公平性的代码来看，头节点就是正在执行的线程，第二个节点进入自旋，其余节点休眠即可。当到第二个节点的线程在执行的时候，我们需要唤醒第三个节点的进程进行自旋。

java 没有直接提供唤醒某个进程的 api，不过我们可以借助 Unsafe 类来实现。

```
public class CLHImproveLock {

    private static Unsafe unsafe;
    static {
        try {
            Field f = Unsafe.class.getDeclaredField("theUnsafe");
            f.setAccessible(true);
            unsafe = (Unsafe) f.get(null);
        }catch (Exception e){
            e.printStackTrace();
        }

    }
    public static class CLHNode {
        private Thread thread;
        private volatile boolean isLocked = true; // 默认是在等待锁

        private volatile CLHNode next;

        public CLHNode(Thread thread) {
            this.thread = thread;
        }

        public Thread getThread() {
            return thread;
        }

        public boolean isLocked() {
            return isLocked;
        }

        public void setLocked(boolean locked) {
            isLocked = locked;
        }

        public CLHNode getNext() {
            return next;
        }

        public void setNext(CLHNode next) {
            this.next = next;
        }
    }

    private volatile CLHNode head;
    private volatile CLHNode tail;

    private static final AtomicReferenceFieldUpdater<CLHImproveLock, CLHNode> UPDATER = AtomicReferenceFieldUpdater
            . newUpdater(CLHImproveLock.class, CLHNode .class , "tail" );
    private static final AtomicReferenceFieldUpdater<CLHImproveLock, CLHNode> UPDATERHEAD = AtomicReferenceFieldUpdater
            . newUpdater(CLHImproveLock.class, CLHNode .class , "head" );

    public void lock(CLHNode currentThread) {
        CLHNode preNode = UPDATER.getAndSet(this,currentThread);
        if(preNode != null) { //已有线程占用了锁，进入自旋
            preNode.next = currentThread;
//            while(preNode.isLocked) {
                while(!currentThread.getThread().isInterrupted()) {// 当前线程没有被中断，则执行
//                    if (preNode != head) {
                    System.out.println(currentThread.getThread().getId() + ";" + currentThread.getThread().isInterrupted());
                        currentThread.getThread().interrupt();
//                    }
//                }
            }
        } else {
            UPDATERHEAD.compareAndSet(this,null,currentThread);
        }
    }

    public void unlock(CLHNode currentThread) {
        currentThread.setLocked(false);// 改变状态，让后续线程结束自旋
        CLHNode clhNode = currentThread.getNext();
        UPDATERHEAD.compareAndSet(this,currentThread,clhNode);
        if(clhNode != null){
            unsafe.unpark(currentThread.getThread());
        }
    }

    public static void main(String[] args) throws Exception{
        final CLHImproveLock lock = new CLHImproveLock();
        CLHNode mainNode = new CLHNode(Thread.currentThread());
        lock.lock(mainNode);

        for (int i = 0; i < 10; i++) {
            new Thread(new Runnable() {
                public void run() {
                    CLHNode tempNode = new CLHNode(Thread.currentThread());
                    lock.lock(tempNode);
                    System.out.println(Thread.currentThread().getId() + " execute");
                    lock.unlock(tempNode);
                }
            }).start();
            Thread.sleep(1000);
        }

        lock.unlock(mainNode);
        System.out.println("main thread unlock! " + mainNode.isLocked);

    }

}
```


