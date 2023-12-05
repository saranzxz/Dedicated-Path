echo "table_add MyIngress.ipv4_lpm MyIngress.forward 192.168.1.0/24 => 00:00:00:00:00:01 0" | simple_switch_CLI
echo "table_add MyIngress.ipv4_lpm MyIngress.forward 192.168.2.0/24 => 00:00:00:00:00:02 1" | simple_switch_CLI
echo "table_add MyIngress.ipv4_lpm MyIngress.forward 192.168.5.0/24 => 00:00:00:00:00:07 1" | simple_switch_CLI

echo "table_add MyIngress.ipv4_lpm_slow MyIngress.forward_slow 192.168.1.0/24 => 192.168.3.10 00:00:00:00:00:07 2" | simple_switch_CLI
