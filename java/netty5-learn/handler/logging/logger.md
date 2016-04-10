# LoggingHandler
LoggingHandler 可以用来记录 netty 的所有事件日志，默认的日志级别时 DEBUG

LoggingHandler 继承 ChannelDuplexHandler，而 ChannelDuplexHandler 则实现了 ChannelInboundHandler 和 ChannelOutboundHandler 的所有操作，所以 LoggingHandler 可以用来记录 netty 中的所有事件日志。

实现方式很简单，就是在每一个事件执行之前打印日志，如 ：
```
public void channelRegistered(ChannelHandlerContext ctx) throws Exception {
    if (logger.isEnabled(internalLevel)) {
        logger.log(internalLevel, format(ctx, "REGISTERED"));
    }
    ctx.fireChannelRegistered();
}
```