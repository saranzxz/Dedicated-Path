echo "table_add MyIngress.ipv4_lpm MyIngress.forward 192.168.3.0/24 => 00:00:00:00:00:03 0" | simple_switch_CLI
echo "table_add MyIngress.ipv4_lpm MyIngress.forward 192.168.5.0/24 => 00:00:00:00:00:08 1" | simple_switch_CLI
