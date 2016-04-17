# Executor 接口

在 java.util.concurrnt 中，Executor 接口属于第一个接口，也是我们需要接触和学习的第一个接口。

查看源码可以知道，Executor 接口的定义很简单:
```
public interface Executor {
  /**
     * Executes the given command at some time in the future.  The command
     * may execute in a new thread, in a pooled thread, or in the calling
     * thread, at the discretion of the <tt>Executor</tt> implementation.
     *
     * @param command the runnable task
     * @throws RejectedExecutionException if this task cannot be
     * accepted for execution.
     * @throws NullPointerException if command is null
     */
    void execute(Runnable command);
}
```

接口定义上说明，Executor 时用来执行一个 Runnable 任务的，这个任务可以在一个线程里执行，或者在线程池里执行，或者直接在当前线程执行，也可以在 Executor 的实现里执行。

下面，分别说明，各种执行情况，先从最简单开始，直接在当前线程执行,如下所示:
```
public class DirectExecutor implements Executor {

    public void execute(Runnable command) {
        command.run();
    }
}
```

深入一点就是在另外一个线程执行:
```
public class NewThreadExecutor implements Executor {

    public void execute(Runnable command) {
        new Thread(command).start();
    }
}
```

深入一点看一下如何在一个线程里执行多个 Runnable，再看串行执行多个 Runnable 的例子:
```
public class SerialExecutor implements Executor {

    final Queue<Runnable> tasks = new ArrayDeque<Runnable>();
    final Thread thread;    // 执行线程
    public SerialExecutor() {
        thread = new Thread(new Runnable() {
            public void run() {
                while (true) {
                    Runnable task = null;
                    if ((task = tasks.poll()) != null) {
                        task.run();
                    }

                    if (task == null) {
                        try {
                            // 当没有任务需要执行了，休眠 1s
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
        });
        thread.start();
    }

    public void execute(Runnable command) {
        tasks.offer(command);
    }
}
```


