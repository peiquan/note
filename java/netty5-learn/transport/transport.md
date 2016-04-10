# transport 的学习
transport 可以看做时 netty 线程模型的主要体现，关于 netty 的线程模型，可以参考 [李林峰 发表的 netty 线程模型](http://www.infoq.com/cn/articles/netty-threading-model/)。这里主要是看一下 netty 的代码实现。

在 netty 中，有一个 EchoServer 的例子，如下:
```
// Configure the server.
EventLoopGroup bossGroup = new NioEventLoopGroup(1);
EventLoopGroup workerGroup = new NioEventLoopGroup();	
try {
    ServerBootstrap b = new ServerBootstrap();
    b.group(bossGroup, workerGroup)
     .channel(NioServerSocketChannel.class)
     .option(ChannelOption.SO_BACKLOG, 100)
     .handler(new LoggingHandler(LogLevel.INFO))
     .childHandler(new ChannelInitializer<SocketChannel>() {
         @Override
         public void initChannel(SocketChannel ch) throws Exception {
             ChannelPipeline p = ch.pipeline();
             p.addLast(new EchoServerHandler());
         }
     });

    // Start the server.
    ChannelFuture f = b.bind(PORT).sync();

    // Wait until the server socket is closed.
    f.channel().closeFuture().sync();
} finally {
    // Shut down all event loops to terminate all threads.
    bossGroup.shutdownGracefully();
    workerGroup.shutdownGracefully();
}
```

从代码上来看，有两个 EeventLoopGroup，当中 bossGroup 可以看做线程模型中 Reactor 线程池，workerGroup 是工作线程池。看一下代码的实现:
```
public ServerBootstrap group(EventLoopGroup parentGroup, EventLoopGroup childGroup) {
    super.group(parentGroup);
    if (childGroup == null) {
        throw new NullPointerException("childGroup");
    }
    if (this.childGroup != null) {
        throw new IllegalStateException("childGroup set already");
    }
    this.childGroup = childGroup;
    return this;
}
```

parentGroup(即 bossGroup) 传到了父类 AbstractBootstrap，查看 AbstractBootstrap 代码，可以知道，AbstractBootstrap 实际上是初始化 Reactor 线程池的。

接下来时:
```
.channel(NioServerSocketChannel.class)
```

用来设置 创建 channel 的工厂类，在服务端的表现就是，当有客户端链接到来时，通过此工厂类创建 channel 对象。


接下来是:
```
.option(ChannelOption.SO_BACKLOG, 100)
```
此处时用来设置 TCP 的相关参数的。



## 参看书籍与文章
[Netty系列之Netty线程模型](http://www.infoq.com/cn/articles/netty-threading-model/)