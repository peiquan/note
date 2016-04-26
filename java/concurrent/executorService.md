# ExecutorService

ExecutorService 属于 Executor 的增强版，提供了多种方法来结束任务的执行和跟踪异步执行的任务。

ExecutorService 可以主动停止，不再接收新任务的执行。shutdown() 方法可以拒绝接收新任务的执行，同时在结束之前会等待之前提交的任务执行完成。而 shutdownNow 除了拒绝执行新任务的之外，也会不再执行之前提交的任务。

## 各种接口的定义

具体接口的定义，可以查看[这里](http://docs.oracle.com/javase/7/docs/api/java/util/concurrent/ExecutorService.html)
