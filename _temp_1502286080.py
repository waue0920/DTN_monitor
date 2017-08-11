import pymongo


client = pymongo.MongoClient("mongodb://peggy:1234@165.124.33.147/test")


db = client.test


 
result = db.dtnInfo.insert_one( { 
"L2cache":"256K",
"hostname":"tcdev004",
"ethernet_nic":"07:00.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01) 07:00.2 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01) 07:00.3 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)",
"BogoMIPS":"4401.15",
"mlx5_core_verion":"2.2-1",
"VendorID":"GenuineIntel",
"CPUs":"24",
"disk_usage":"199/3GB (6%)",
"CPU_load":"0.00",
"NUMAnodes":"2",
"OnlineCPUslist":"0-23",
"L3cache":"15360K",
"net_ipv4_wmem_max":"212992",
"Architecture":"x86_64",
"CPUfamily":"6",
"Sockets":"2",
"Virtualization":"VT-x",
"ip_arr":"172.16.1.40 140.110.141.164 2001:e10:6040:141:42f2:e9ff:fe68:c6d3 ",
"irq_balance_status":"start/running,",
"CPUMHz":"1803.742",
"Stepping":"7",
"Corespersocket":"6",
"net_ipv5_tcp_mtu_probing":"0",
"Model":"45",
"net_ipv4_tcp_wmem":"4096 16384 4194304",
"net_core_rmem_max":"212992",
"ByteOrder":"Little Endian",
"net_ipv4_tcp_congestion_control":"cubic",
"net_ipv4_tcp_rmem":"4096 87380 6291456",
"CPUopmodes":"32-bit, 64-bit",
"vm":"Intel Corporation",
"L1icache":"32K",
"memory_usage":"47735/48276MB (98.88%)",
"NUMAnode1CPUs":"6-11,18-23",
"L1dcache":"32K",
"Threadspercore":"2",
"NUMAnode0CPUs":"0-5,12-17"
} )
