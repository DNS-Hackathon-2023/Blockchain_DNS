$ORIGIN nlnetlabs.nl.
$TTL 1800

nlnetlabs.nl.	          1800 IN        SOA	japp.nlnetlabs.nl. dnsadmin.nlnetlabs.nl. 21377098 900 600 86400 3600

nlnetlabs.nl.            10200  IN         A    185.49.140.10
nlnetlabs.nl.		       240	IN	    AAAA	2a04:b900::1:0:0:10

nlnetlabs.nl.		       240	IN	      MX	1 mx.soverin.net.
nlnetlabs.nl.		       240	IN	     TXT	"v=spf1 +a include:soverin.net include:_spf.google.com ip4:185.49.140.0/22 ip6:2a04:b900::/29 ~all"
nlnetlabs.nl.		       240	IN	     TXT	"Soverin=xxXyBKG251ppd1JT"
nlnetlabs.nl.		       240	IN	     TXT	"Stichting NLnet Labs zone"


blog.nlnetlabs.nl.       10200    IN   CNAME    nlnetlabs.ghost.io.
smtp.nlnetlabs.nl.         240    IN   CNAME    open.nlnetlabs.nl.
behemoth.nlnetlabs.nl.   10200    IN   CNAME    behemoth.overeinder.net.

dmz.nlnetlabs.nl.        10200    IN       A    185.49.141.1
dmz.nlnetlabs.nl.	      1800    IN	AAAA	2a04:b900:0:100::1

lists.nlnetlabs.nl.        240    IN       A    185.49.141.25
lists.nlnetlabs.nl.	       240    IN	AAAA	2a04:b900:0:100::25

mx.nlnetlabs.nl.           240    IN       A    89.58.15.138
mx.nlnetlabs.nl.	       240    IN	AAAA	2a03:4000:60:db7:24ea:24ff:fe95:d10a

ns.nlnetlabs.nl.         10200    IN       A    185.49.140.60
ns.nlnetlabs.nl.	      1800    IN	AAAA	2a04:b900::8:0:0:60

ns1.nlnetlabs.nl.        10200    IN       A    185.49.140.10
ns1.nlnetlabs.nl.	      1800	  IN	AAAA	2a04:b900::1:0:0:10

office.nlnetlabs.nl.     10200    IN       A    185.49.140.113
office.nlnetlabs.nl.	  1800	  IN	AAAA	2a04:b900::10:0:0:113

pan.nlnetlabs.nl.        10200    IN       A    185.49.140.130
pan.nlnetlabs.nl.	      1800	  IN	AAAA	2a04:b900::21c:c0ff:fe11:b9b8

open.nlnetlabs.nl.       10200    IN       A    185.49.140.10
open.nlnetlabs.nl.	      1800	  IN	AAAA	2a04:b900::1:0:0:10

www.nlnetlabs.nl.        10200    IN       A    185.49.140.10
www.nlnetlabs.nl.	      1800    IN	AAAA	2a04:b900::1:0:0:10

