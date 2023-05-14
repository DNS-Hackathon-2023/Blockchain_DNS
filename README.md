# Blockchain_DNS

## Description
A DNS Authority Namserver, BCDNS,  has been written as a smart contract on the ethereum blockchain.  This DNS Nameserver provides:
* decentralization: high availability, DDoS and censorship resistant
* data security: all records are digitally signed, but much simpler to use than DNSSEC
* data privacy: all lookups and data retrieval are HTTPS encrypted

See the BCDNS paper for more details on what the implementation does and how it works.

## Experiments you can try right now
Several bridges from BCDNS to conventional DNS have already been written and are running in the Amazon cloud.  
* UNBOUND plugin: 
  *  Try doing a dig command to the UNBOUND resolver running at IP address 35.89.75.91 for A, AAAA, MX, TXT or other types.
  *  Example:  dig @35.89.75.91 nlnetlabs.nl AAAA.      Notice that the response has the AD bit set because it is digitally signed on the blockchain
  *  Example:  do a dig for mit.edu (not in the blockchain).  UNBOUND does normal resolution if nothing found in the blockchain and returns the answer, but the AD bit is not set.
  *  Examine the sample zone files for other possible domain names and RRTypes to dig.
* Port53Proxy:  This is a simple, non-caching converter of UDP DNS requests to retrieve data from the blockchain.  Listening at 54.159.243.13
  * Example:  dig @54.159.243.13.   Try MX and TXT as well.
  * There is no caching and no other resolution.  If the domain is not in the blockchain it will return NXDOMAIN.
* ./bcdig domainname -- a python program that does a direct to blockchain lookup with output that emulates the dig command.

## Hackathon Project Ideas
* Ideas that could be done in a weekend:
  1. Modify DNSMasq or ConnectByName to retrieve DNS data from blockchain; if No Data, do normal DNS lookup. Cache the data.
  2. Build BC plugins for KNOT Resolver or PowerDNS. Unbound plugin is already written.
* Ideas that are worthwhile, but probably too big for a weekend
  1. Modify Mozilla TRR (trusted resolver) to directly access the blockchain
  2. Mobile adaptor for blockchain 

<img src="/images/Hackathon_Ideas.png" alt="Hackathon Ideas" width="1200" />

## BCDNS EcoSystem

<img src="/images/POC Architecture.png" alt="ecosystem" width="1200" />


