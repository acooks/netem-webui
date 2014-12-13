class Netstats(object):

   def __init__(self, ifaces):
      self.ifaces = ifaces
      self.counts = dict()
      self.counts["old"] = dict()


   def get_stats(self):
      self.update_stats()
      return self.counts["cur"]


   def update_stats(self):
      with open('/proc/net/dev', 'r') as f:
         raw_counters = f.read()
         parsed_cumulative_counts = self.parse_counters(raw_counters)
         self.calc_instant_stats(parsed_cumulative_counts)


   def parse_counters(self, raw_counters):
      iface_bytes = dict()
      # rawstats has two lines of header and then one line per iface.
      for line in raw_counters.split('\n'):
         # lines containing iface stats start with 'iface:'
         split_iface = line.split(':')
         if (len(split_iface) > 1):
            iface = split_iface[0].strip()
            # after 'iface:' comes data cols. RX, then TX
            # RX: bytes, pckts, errs, drop, fifo, frame, compressed, multicast
            # TX: bytes, pckts, errs, drop, fifo, colls, carrier, compressed
            split_data = split_iface[1].split()
            rx_bytes, tx_bytes = (split_data[0], split_data[8])
            iface_bytes[iface] = (int(rx_bytes.strip()), int(tx_bytes.strip()))
      return iface_bytes


   def calc_instant_stats(self, cur_counts):
      # cur_counts is the current counter values, like
      #  {'iface1': [rx-bytes, tx-bytes], 'iface2': [rx-bytes, tx_bytes]}
      self.counts["cur"] = dict()
      for iface in self.ifaces:
         # short aliases hopefully helps readability
         c_rx = cur_counts[iface][0]
         c_tx = cur_counts[iface][1]

         # initialise counts on start-up
         if not iface in self.counts["old"]:
            self.counts["old"][iface] = dict()
            self.counts["old"][iface]["rx-bytes"] = c_rx
            self.counts["old"][iface]["tx-bytes"] = c_tx

         self.counts["cur"][iface] = dict()
         cnt = self.counts["cur"][iface] # short alias
         o_cnt = self.counts["old"][iface] # short alias

         cnt["rx-bytes"] = c_rx - int(0.5 * (c_rx + o_cnt["rx-bytes"]))
         cnt["tx-bytes"] = c_tx - int(0.5 * (c_tx + o_cnt["tx-bytes"]))

         o_cnt["rx-bytes"] = c_rx
         o_cnt["tx-bytes"] = c_tx

      # print self.counts["cur"]
      # self.counts now looks something like:
      # {'old': {'iface1': {'rx-bytes': rx-bytes1, 'tx-bytes': tx-bytes1},
      #          'iface2': {'rx-bytes': rx-bytes2, 'tx-bytes': tx-bytes2}},
      #  'new': {'iface1': {'rx-bytes': rx-bytes3, 'tx-bytes': tx-bytes3},
      #          'iface2': {'rx-bytes': rx-bytes4, 'tx-bytes': tx-bytes4}}
      # }
