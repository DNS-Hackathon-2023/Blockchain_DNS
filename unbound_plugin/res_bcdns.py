'''
 res_bcdns.py: This example shows how to generate authoritative response
               from blockchain

 Copyright (c) 2023, Joseph Gersch (jgersch@invykta.com)

 This software is open source.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

    * Neither the name of the organization nor the names of its
      contributors may be used to endorse or promote products derived from this
      software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE
 LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
'''

import os
import json
import zlib
from struct import unpack
from web3 import Web3


# from dotenv import load_dotenv

#############################################################################################
#   BCdig class:    data and methods to do a DNS dig to the blockchain
#############################################################################################

class BCDNS:

    def __init__(self):
        self.w3 = None
        self.contract = None
        self.provider = "https://arb-goerli.g.alchemy.com/v2/hZ_CO-C_VCPy62nk6K98qcVM5f75G0qV"
        # self.provider = "https://104.18.40.62/v2/hZ_CO-C_VCPy62nk6K98qcVM5f75G0qV"
        self.contract_address = "0x7FeB8CE8baAea22cE0E922cC7cc9f62367Bf7280"
        self.abi = '''{"abi": [{
          "inputs": [
            {
              "internalType": "string",
              "name": "_FQDN",
              "type": "string"
            }
          ],
          "name": "getRRset",
          "outputs": [
            {
              "internalType": "bytes",
              "name": "RRsetMF",
              "type": "bytes"
            }
          ],
          "stateMutability": "view",
          "type": "function"
        }]}
        '''

    #########################################################################################
    #   Method to connect to blockchain and DDNS smart contract
    #           Note: these constants will change if using a new smart contract or blockchain
    #########################################################################################

    def initBC(self):
        # load_dotenv()
        try:
            log_info("init %s %s" % (self.provider, self.contract_address))
            self.w3 = Web3(Web3.HTTPProvider(self.provider))
            log_info("w3 %s" % (str(self.w3)))
            # if not self.w3.is_connected(): raise Exception
            # use a subset of the ABI instead of reading the whole ABI contents from a file
            abi = json.loads(self.abi)
            self.contract = self.w3.eth.contract(address=self.contract_address, abi=abi["abi"])
        except Exception as err:
            log_info("**** Error: unable to connect to blockchain; program terminated")
            log_info(str(err))
            exit(1)

    ###################################################################
    # convertToCanonical:  converts multiformat encoded RRset to array of DNS canonical strings
    ###################################################################

    def convertToCanonical(self, qinfo, mf):
        data = mf
        fmt = "@c" + str(len(mf) - 1) + "s"
        encoder, data = unpack(fmt, mf)
        canonical = []

        if encoder == b'\x00': return canonical  # delegation

        if encoder in [b'\x02', b'\x04']:
            # zip encoded.  Decompress it.
            data = zlib.decompress(data)

        # build the canonical form for the requested rrType
        data = data.decode('ascii')
        if encoder in [b'\x01', b'\x02']:
            # tinyJSON
            data = json.loads(data)
            key = str(qinfo.qtype)
            if key in data:
                d = data[key]
                log_info("boop %s" % (str(d)))
                for rdata in d[2]:
                    canonical.append(" ".join((qinfo.qname_str, str(d[0]), qinfo.qclass_str, qinfo.qtype_str, rdata)))
        else:
            # already in canonical RRset form
            if data.split("\t")[2] == qinfo.qtype_str:
                for rdata in data.split("\n")[0:-1]:  # split will put a blank last entry, so don't use it
                    canonical.append(qinfo.qname_str + " " + rdata)
        return canonical


def init(id, cfg):
    log_info("pythonmod: init called, module id is %d port: %d script: %s" % (id, cfg.port, cfg.python_script))
    bcdns.initBC()
    return True


def deinit(id): return True


def inform_super(id, qstate, superqstate, qdata): return True


def operate(id, event, qstate, qdata):
    if (event == MODULE_EVENT_NEW) or (event == MODULE_EVENT_PASS):
        try:
            log_info("**** bcdns for %s" % (qstate.qinfo.qname_str))
            rrsetMF = bcdns.contract.functions.getRRset(qstate.qinfo.qname_str).call()
            log_info("**** got some BC data")
            log_info("**** BC found data %s" % (str(rrsetMF)))
            rrsets = bcdns.convertToCanonical(qstate.qinfo, rrsetMF)
            log_info("**** data %s" % (rrsets))
            # create instance of DNS message (packet) with given parameters
            # msg = DNSMessage(qstate.qinfo.qname_str, qstate.qinfo.qtype, qstate.qinfo.qclass, PKT_QR | PKT_RA | PKT_AA | PKT_AD)
            msg = DNSMessage(qstate.qinfo.qname_str, qstate.qinfo.qtype, qstate.qinfo.qclass, PKT_QR | PKT_RA | PKT_AD)
            # append RRs
            for rrset in rrsets:
                msg.answer.append(rrset)
            # set qstate.return_msg
            if not msg.set_return_msg(qstate):
                qstate.ext_state[id] = MODULE_ERROR
                return True

            # we don't need validation, result is valid
            qstate.return_msg.rep.security = 2

            qstate.return_rcode = RCODE_NOERROR
            qstate.ext_state[id] = MODULE_FINISHED
            log_info("wire name: %s" % (qstate.return_msg.qinfo.qname.hex()))
            log_info("flags: %d" % (qstate.return_msg.rep.flags))
            log_info("qdcount: %d" % (qstate.return_msg.rep.qdcount))
            log_info("ttl: %d" % (qstate.return_msg.rep.ttl))
            log_info("security: %d" % (qstate.return_msg.rep.security))
            log_info("an_numrrsets: %d" % (qstate.return_msg.rep.an_numrrsets))
            log_info("rrset_count: %d" % (qstate.return_msg.rep.rrset_count))
            # qstate.no_cache_store = True
            log_info("cacheflag: %d" % (qstate.no_cache_store))
            log_info("cacheflaglookup: %d" % (qstate.no_cache_lookup))
            # log_info("rrset id: %d" % (qstate.return_msg.rep.rrsets[0].id))
            # log_info("rrset entry data count: %d" % (qstate.return_msg.rep.rrsets[0].entry.data.count))
            # log_info("rrset entry data trust: %d" % (qstate.return_msg.rep.rrsets[0].entry.data.trust))
            # log_info("rrset entry data security: %d" % (qstate.return_msg.rep.rrsets[0].entry.data.security))
            # log_info("rrset entry data rrlen[0]: %d" % (qstate.return_msg.rep.rrsets[0].entry.data.rr_len[0]))
            # log_info("rrset entry data rrttl[0]: %d" % (qstate.return_msg.rep.rrsets[0].entry.data.rr_ttl[0]))
            # log_info("wd: %s" % ( str(qstate.return_msg.rep.rrsets[0].entry.data.rr_data[0][0:6].hex())))
            try:
                storeQueryInCache(qstate, qstate.qinfo, qstate.return_msg.rep, False)
            except Exception as err:
                log_info("error msg: %s" % (err))
            return True
        except:
            # pass the query to validator
            log_info("**** BC lookup failed")
            qstate.ext_state[id] = MODULE_WAIT_MODULE
            return True

    if event == MODULE_EVENT_MODDONE:
        log_info("pythonmod: iterator module done")
        qstate.ext_state[id] = MODULE_FINISHED
        return True

    log_err("pythonmod: bad event")
    qstate.ext_state[id] = MODULE_ERROR
    return True


bcdns = BCDNS()
log_info("pythonmod: script loaded.")