; Domain: invykta.com
; Exported (y-m-d hh:mm:ss): 2022-08-22 10:00:23
;
; This file is intended for use for informational and archival
; purposes ONLY and MUST be edited before use on a production
; DNS server.
;
; In particular, you must update the SOA record with the correct
; authoritative name server and contact e-mail address information,
; and add the correct NS records for the name servers which will
; be authoritative for this domain.
;
; For further information, please consult the BIND documentation
; located on the following website:
;
; http://www.isc.org/
;
; And RFC 1035:
;
; http://www.ietf.org/rfc/rfc1035.txt
;
; Please note that we do NOT offer technical support for any use
; of this zone data, the BIND name server, or any other third-
; party DNS software.
;
; Use at your own risk.


$ORIGIN invykta.com.

; SOA Record
@	600	 IN 	SOA	ns71.domaincontrol.com.	dns.jomax.net. (
					2022081800
					28800
					7200
					604800
					600
					) 

; A Record
@       1800	IN	    A	13.248.243.5
@		1800	IN	    A	76.223.105.230
test	1800	 IN 	A	192.168.0.2
test	1800	 IN 	A	192.168.0.1

; TXT Record
@	600	 IN 	TXT	"NETORGFT3464545.onmicrosoft.com"
@	600	 IN 	TXT	"v=spf1 include:spf.protection.outlook.com -all"
test	3600	 IN 	TXT	"This is a test"
_acme-challenge	3600	 IN 	TXT	"xcEkt8lrOUYnOvmSOWK2OT3kFwMbMfC7mfX-VazzjhE"

; CNAME Record
autodiscover	600	 IN 	CNAME	autodiscover.outlook.com.
email	600	 IN 	CNAME	email.secureserver.net.
ftp	3600	 IN 	CNAME	@
lyncdiscover	600	 IN 	CNAME	webdir.online.lync.com.
msoid	600	 IN 	CNAME	clientconfig.microsoftonline-p.net.
sip	600	 IN 	CNAME	sipdir.online.lync.com.
www	3600	 IN 	CNAME	@
_domainconnect	3600	 IN 	CNAME	_domainconnect.gd.domaincontrol.com.

; SRV Record
_sip._tls	                1800	 IN 	SRV	100	1	443	sipdir.online.lync.com.
_sipfederationtls._tcp	    1800	 IN 	SRV	100	1	5061	sipfed.online.lync.com.

; NS Record
@	3600	 IN 	NS	ns71.domaincontrol.com.
@	3600	 IN 	NS	ns72.domaincontrol.com.

; MX Record
@	600	 IN 	MX	0	invykta-com.mail.protection.outlook.com.

; fake CERT records
joe.gersch.certs TXT "joe gersch"
karen.gersch.certs TXT "karen gersch"
kevin.gersch.certs TXT "kevin gersch"
kimi.gersch.certs TXT "kimi gersch"
karen.gersch.certs TXT "karen gersch"
lily.gersch.certs TXT "lily gersch"
logan.gersch.certs TXT "logan gersch"
david.roth.certs TXT "david roth"

; department servers
gandalf.lab 3600 IN A 10.0.0.1
bilbo.lab   3600 IN A 10.0.0.2
samwise.lab 3600 IN A 10.0.0.3
gollum.lab  3600 IN A 10.0.0.4

dopey.sales 3600 IN A 10.0.1.1
sneezy.sales 3600 IN A 10.0.1.2
doc.sales    3600 IN A 10.0.1.3

cindy.mktg  3600 IN A 10.0.2.1
lily.mktg   3600 IN A 10.0.2.2
logan.mktg  3600 IN A 10.0.2.3
kevin.mktg  3600 IN A 10.0.2.4

kimi.support 3600 IN A 10.0.3.1
pierrick.support 3600 IN A 10.0.3.2
zachary.support  3600 IN A 10.0.3.3

;STUPID 3600 IN TXT "delete me"