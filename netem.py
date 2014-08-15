import subprocess

class Netem(object):

   def __init__(self):
      pass

   def get_netem(self, dev):
      assert dev
      print dev
      args = ['tc', 'qdisc', 'show', 'dev', dev]
      print args
      p = subprocess.Popen(args, stdout=subprocess.PIPE)
      output = p.communicate()[0]
            
      return self.parse_tc(output)


   def parse_tc(self, tc_string):
      val = {'conf': tc_string, 'delay':'0', 'd_var':'0', 'd_cor':'0',
             'loss':'0', 'l_cor':'0'};

      parts = tc_string.split()
      print(parts)

      if len(parts) > 11:
        val['delay'] = parts[9]
        val['d_var'] = parts[10]
        val['d_cor'] = parts[11]
        val['loss']  = parts[13]
        val['l_cor'] = parts[14]
        print(val)
      return val;


   def set_delay(self, dev, d_size, d_variation=0, d_correlation=1,
                 loss='0.001%', l_cor='0.001%'):
      assert dev
      print ("dev: [%s] delay: [%s] d_variation: [%s] d_correlation: [%s]" \
             % (dev, d_size, d_variation, d_correlation))
      args = ['tc', 'qdisc', 'change', 'dev', dev, 'root', 'netem', 'delay',
              d_size, d_variation, d_correlation, 'distribution', 'normal',
              'loss', loss, l_cor]
      print args
      p = subprocess.Popen(args, stdout=subprocess.PIPE)
      return self.get_netem(dev)
      

