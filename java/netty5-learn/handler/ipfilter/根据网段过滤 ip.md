# 根据网段过滤 ip
在 netty 中，提供了对应的 iP handler，允许用户根据网段来过滤 ip，可以过滤允许访问的 ip，也可以过滤不可以访问的 ip。

原理： 指定一个网段(可知当前网段的网络号和子网掩码）， 给定一个 ip，若当前 ip 与 子网掩码相与得到网络号，若求出的网络号与已知网络号相同，即认为当前 ip 匹配指定规则。

netty 中的具体实现:
```
// ip 过滤的类型，接受或拒绝
public enum IpFilterRuleType {
    ACCEPT,
    REJECT
}
```

// 接口的定义
```
public interface IpFilterRule {
    /**
     * 返回当前 ip 是否匹配指定网络段
     */
    boolean matches(InetSocketAddress remoteAddress);

    /* 当输入 ip 匹配之后，是可以访问，还是拒绝访问 */
    IpFilterRuleType ruleType();
}
```

// 实现
```
import java.math.BigInteger;
import java.net.Inet4Address;
import java.net.Inet6Address;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.UnknownHostException;

/**
 * Use this class to create rules for {@link RuleBasedIpFilter} that group IP addresses into subnets.
 * Supports both, IPv4 and IPv6.
 */
public final class IpSubnetFilterRule implements IpFilterRule {

    private final IpFilterRule filterRule;

    public IpSubnetFilterRule(String ipAddress, int cidrPrefix, IpFilterRuleType ruleType) {
        try {
            filterRule = selectFilterRule(InetAddress.getByName(ipAddress), cidrPrefix, ruleType);
        } catch (UnknownHostException e) {
            throw new IllegalArgumentException("ipAddress", e);
        }
    }

    public IpSubnetFilterRule(InetAddress ipAddress, int cidrPrefix, IpFilterRuleType ruleType) {
        filterRule = selectFilterRule(ipAddress, cidrPrefix, ruleType);
    }

    private static IpFilterRule selectFilterRule(InetAddress ipAddress, int cidrPrefix, IpFilterRuleType ruleType) {
        if (ipAddress == null) {
            throw new NullPointerException("ipAddress");
        }

        if (ruleType == null) {
            throw new NullPointerException("ruleType");
        }

        if (ipAddress instanceof Inet4Address) {
            return new Ip4SubnetFilterRule((Inet4Address) ipAddress, cidrPrefix, ruleType);
        } else if (ipAddress instanceof Inet6Address) {
            return new Ip6SubnetFilterRule((Inet6Address) ipAddress, cidrPrefix, ruleType);
        } else {
            throw new IllegalArgumentException("Only IPv4 and IPv6 addresses are supported");
        }
    }

    @Override
    public boolean matches(InetSocketAddress remoteAddress) {
        return filterRule.matches(remoteAddress);
    }

    @Override
    public IpFilterRuleType ruleType() {
        return filterRule.ruleType();
    }

    private static final class Ip4SubnetFilterRule implements IpFilterRule {

        private final int networkAddress;
        private final int subnetMask;
        private final IpFilterRuleType ruleType;

        private Ip4SubnetFilterRule(Inet4Address ipAddress, int cidrPrefix, IpFilterRuleType ruleType) {
            if (cidrPrefix < 0 || cidrPrefix > 32) {
                throw new IllegalArgumentException(String.format("IPv4 requires the subnet prefix to be in range of " +
                                                                    "[0,32]. The prefix was: %d", cidrPrefix));
            }

            subnetMask = prefixToSubnetMask(cidrPrefix);
            networkAddress = ipToInt(ipAddress) & subnetMask;
            this.ruleType = ruleType;
        }

        @Override
        public boolean matches(InetSocketAddress remoteAddress) {
            int ipAddress = ipToInt((Inet4Address) remoteAddress.getAddress());

            return (ipAddress & subnetMask) == networkAddress;
        }

        @Override
        public IpFilterRuleType ruleType() {
            return ruleType;
        }

        private static int ipToInt(Inet4Address ipAddress) {
            byte[] octets = ipAddress.getAddress();
            assert octets.length == 4;

            return (octets[0] & 0xff) << 24 |
                   (octets[1] & 0xff) << 16 |
                   (octets[2] & 0xff) << 8 |
                    octets[3] & 0xff;
        }

        private static int prefixToSubnetMask(int cidrPrefix) {
            /**
             * Perform the shift on a long and downcast it to int afterwards.
             * This is necessary to handle a cidrPrefix of zero correctly.
             * The left shift operator on an int only uses the five least
             * significant bits of the right-hand operand. Thus -1 << 32 evaluates
             * to -1 instead of 0. The left shift operator applied on a long
             * uses the six least significant bits.
             *
             * Also see https://github.com/netty/netty/issues/2767
             */
            return (int) ((-1L << 32 - cidrPrefix) & 0xffffffff);
        }
    }

    private static final class Ip6SubnetFilterRule implements IpFilterRule {

        private static final BigInteger MINUS_ONE = BigInteger.valueOf(-1);

        private final BigInteger networkAddress;
        private final BigInteger subnetMask;
        private final IpFilterRuleType ruleType;

        private Ip6SubnetFilterRule(Inet6Address ipAddress, int cidrPrefix, IpFilterRuleType ruleType) {
            if (cidrPrefix < 0 || cidrPrefix > 128) {
                throw new IllegalArgumentException(String.format("IPv6 requires the subnet prefix to be in range of " +
                                                                    "[0,128]. The prefix was: %d", cidrPrefix));
            }

            subnetMask = prefixToSubnetMask(cidrPrefix);
            networkAddress = ipToInt(ipAddress).and(subnetMask);
            this.ruleType = ruleType;
        }

        @Override
        public boolean matches(InetSocketAddress remoteAddress) {
            BigInteger ipAddress = ipToInt((Inet6Address) remoteAddress.getAddress());

            return ipAddress.and(subnetMask).equals(networkAddress);
        }

        @Override
        public IpFilterRuleType ruleType() {
            return ruleType;
        }

        private static BigInteger ipToInt(Inet6Address ipAddress) {
            byte[] octets = ipAddress.getAddress();
            assert octets.length == 16;

            return new BigInteger(octets);
        }

        private static BigInteger prefixToSubnetMask(int cidrPrefix) {
            return MINUS_ONE.shiftLeft(128 - cidrPrefix);
        }
    }
}
```

整体处理，本人基本时清楚的，不过不太理解的时，为什么子网掩码是这样求的，并且如下方法求出来的并不是子网掩码:
```
 private static int prefixToSubnetMask(int cidrPrefix) {
    /**
     * Perform the shift on a long and downcast it to int afterwards.
     * This is necessary to handle a cidrPrefix of zero correctly.
     * The left shift operator on an int only uses the five least
     * significant bits of the right-hand operand. Thus -1 << 32 evaluates
     * to -1 instead of 0. The left shift operator applied on a long
     * uses the six least significant bits.
     *
     * Also see https://github.com/netty/netty/issues/2767
     */
    return (int) ((-1L << 32 - cidrPrefix) & 0xffffffff);
}
```

做一个备注，待后续再深入了解