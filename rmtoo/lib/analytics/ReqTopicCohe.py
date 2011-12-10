'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Coherence of one requirement to the used topic.
   
 (c) 2010-2011 by flonatel GmhH & Co. KG

 For licensing details see COPYING
'''

from rmtoo.lib.analytics.Result import Result

class ReqTopicCohe:

    def __init__(self, config):
        '''Sets up the ReqTopicCohe object for use.'''
        pass

    @staticmethod
    def count_in_out_topic(topic, li):
        '''Count the number of incoming and outgoing links.'''
        in_cnt = 0
        out_cnt = 0
        for l in li:
            if l.get_value("Topic") == topic:
                in_cnt += 1
            else:
                out_cnt += 1
        return in_cnt, out_cnt

    def check_requirement(self, lname, requirement):
        '''Check the topic coherence.'''
        it_in, it_out = ReqTopicCohe.count_in_out_topic(
                requirement.get_value("Topic"), requirement.incoming)
        ot_in, ot_out = ReqTopicCohe.count_in_out_topic(
                requirement.get_value("Topic"), requirement.outgoing)

        # This is only problematic, if the in and out are not
        # really coherent to the topic.
        if it_in < it_out and ot_in < ot_out:
            return False, Result('ReqTopicCoherence', lname,
                  - 10, ["Requirement topic coherence inadequate: "
                           "incoming %d/%d, outgoing %d/%d"
                           % (it_in, it_out, ot_in, ot_out)])

        return True, []
