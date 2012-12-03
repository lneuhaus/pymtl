#=========================================================================
# TorusRouter
#=========================================================================

from   pymtl import *
import pmlib

from math import ceil, log

from pmlib.net_msgs    import NetMsgParams
from NormalQueue       import NormalQueue
from pmlib.queues      import SingleElementPipelinedQueue
from InputTermCtrl     import InputTermCtrl
from InputRowCtrl      import InputRowCtrl
from InputColCtrl      import InputColCtrl
from OutputCtrl        import OutputCtrl
from Crossbar5         import Crossbar5

class TorusRouterCtrl (Model):

  @capture_args
  def __init__( s, router_x_id, router_y_id,  num_routers,  num_messages,
    payload_nbits, num_entries ):

    # Local Parameters

    credit_nbits    = int( ceil( log( num_entries+1, 2 ) ) )
    s.netmsg_params = NetMsgParams( num_routers, num_messages, payload_nbits )

    #---------------------------------------------------------------------
    # Interface Ports
    #---------------------------------------------------------------------

    # Port 0 - North

    s.dest0         = InPort  ( s.netmsg_params.srcdest_nbits )
    s.in0_deq_val   = InPort  ( 1 )
    s.in0_deq_rdy   = OutPort ( 1 )
    s.in0_credit    = OutPort ( 1 )
    s.out0_val      = OutPort ( 1 )
    s.xbar_sel0     = OutPort ( 3 )
    s.out0_credit   = InPort  ( 1 )

    # Port 1 - East

    s.dest1         = InPort  ( s.netmsg_params.srcdest_nbits )
    s.in1_deq_val   = InPort  ( 1 )
    s.in1_deq_rdy   = OutPort ( 1 )
    s.in1_credit    = OutPort ( 1 )
    s.out1_val      = OutPort ( 1 )
    s.xbar_sel1     = OutPort ( 3 )
    s.out1_credit   = InPort  ( 1 )

    # Port 2 - South

    s.dest2         = InPort  ( s.netmsg_params.srcdest_nbits )
    s.in2_deq_val   = InPort  ( 1 )
    s.in2_deq_rdy   = OutPort ( 1 )
    s.in2_credit    = OutPort ( 1 )
    s.out2_val      = OutPort ( 1 )
    s.xbar_sel2     = OutPort ( 3 )
    s.out2_credit   = InPort  ( 1 )

    # Port 3 - West

    s.dest3         = InPort  ( s.netmsg_params.srcdest_nbits )
    s.in3_deq_val   = InPort  ( 1 )
    s.in3_deq_rdy   = OutPort ( 1 )
    s.in3_credit    = OutPort ( 1 )
    s.out3_val      = OutPort ( 1 )
    s.xbar_sel3     = OutPort ( 3 )
    s.out3_credit   = InPort  ( 1 )

    # Port 4 - Terminal

    s.dest4         = InPort  ( s.netmsg_params.srcdest_nbits )
    s.in4_deq_val   = InPort  ( 1 )
    s.in4_deq_rdy   = OutPort ( 1 )
    s.in4_credit    = OutPort ( 1 )
    s.out4_val      = OutPort ( 1 )
    s.xbar_sel4     = OutPort ( 3 )
    s.out4_credit   = InPort  ( 1 )

    # Wires

    s.inreqs0       = Wire ( 5 )
    s.inreqs1       = Wire ( 5 )
    s.inreqs2       = Wire ( 5 )
    s.inreqs3       = Wire ( 5 )
    s.inreqs4       = Wire ( 5 )

    s.ingrants0     = Wire ( 5 )
    s.ingrants1     = Wire ( 5 )
    s.ingrants2     = Wire ( 5 )
    s.ingrants3     = Wire ( 5 )
    s.ingrants4     = Wire ( 5 )

    s.outreqs0      = Wire ( 5 )
    s.outreqs1      = Wire ( 5 )
    s.outreqs2      = Wire ( 5 )
    s.outreqs3      = Wire ( 5 )
    s.outreqs4      = Wire ( 5 )

    s.outgrants0    = Wire ( 5 )
    s.outgrants1    = Wire ( 5 )
    s.outgrants2    = Wire ( 5 )
    s.outgrants3    = Wire ( 5 )
    s.outgrants4    = Wire ( 5 )

    #---------------------------------------------------------------------
    # Static elaboration
    #---------------------------------------------------------------------

    # InputCtrl - North Port

    s.inctrl_north = m = InputColCtrl( router_x_id, router_y_id, num_routers,
                          s.netmsg_params.srcdest_nbits, credit_nbits, num_entries )
    connect({
      m.dest      : s.dest0,
      m.deq_val   : s.in0_deq_val,
      m.deq_rdy   : s.in0_deq_rdy,
      m.in_credit : s.in0_credit,
    })

    # InputCtrl - East Port

    s.inctrl_east = m = InputRowCtrl( router_x_id, router_y_id, num_routers,
                          s.netmsg_params.srcdest_nbits, credit_nbits, num_entries )
    connect({
      m.dest      : s.dest1,
      m.deq_val   : s.in1_deq_val,
      m.deq_rdy   : s.in1_deq_rdy,
      m.in_credit : s.in1_credit,
    })

    # InputCtrl - South Port

    s.inctrl_south = m = InputColCtrl( router_x_id, router_y_id, num_routers,
                           s.netmsg_params.srcdest_nbits, credit_nbits, num_entries )
    connect({
      m.dest      : s.dest2,
      m.deq_val   : s.in2_deq_val,
      m.deq_rdy   : s.in2_deq_rdy,
      m.in_credit : s.in2_credit,
    })

    # InputCtrl - West Port

    s.inctrl_west = m = InputRowCtrl( router_x_id, router_y_id, num_routers,
                          s.netmsg_params.srcdest_nbits, credit_nbits, num_entries )
    connect({
      m.dest      : s.dest3,
      m.deq_val   : s.in3_deq_val,
      m.deq_rdy   : s.in3_deq_rdy,
      m.in_credit : s.in3_credit,
    })

    # InputCtrl - Terminal Port

    s.inctrl_term = m = InputTermCtrl( router_x_id, router_y_id, num_routers,
                          s.netmsg_params.srcdest_nbits, credit_nbits, num_entries )
    connect({
      m.dest      : s.dest4,
      m.deq_val   : s.in4_deq_val,
      m.deq_rdy   : s.in4_deq_rdy,
      m.in_credit : s.in4_credit,
    })

    # Output Ctrl - North Port

    s.outctrl_north = m = OutputCtrl(  num_entries,
                            credit_nbits )
    connect({
      m.credit   : s.out0_credit,
      m.xbar_sel : s.xbar_sel0,
      m.out_val  : s.out0_val
    })

    # Output Ctrl - East Port

    s.outctrl_east = m = OutputCtrl(  num_entries,
                           credit_nbits )
    connect({
      m.credit   : s.out1_credit,
      m.xbar_sel : s.xbar_sel1,
      m.out_val  : s.out1_val
    })

    # Output Ctrl - South Port

    s.outctrl_south = m = OutputCtrl(  num_entries,
                            credit_nbits )
    connect({
      m.credit   : s.out2_credit,
      m.xbar_sel : s.xbar_sel2,
      m.out_val  : s.out2_val
    })

    # Output Ctrl - West Port

    s.outctrl_west = m = OutputCtrl(  num_entries,
                           credit_nbits )
    connect({
      m.credit   : s.out3_credit,
      m.xbar_sel : s.xbar_sel3,
      m.out_val  : s.out3_val
    })

    # Output Ctrl - Terminal Port

    s.outctrl_term = m = OutputCtrl( num_entries,
                           credit_nbits )
    connect({
      m.credit   : s.out4_credit,
      m.xbar_sel : s.xbar_sel4,
      m.out_val  : s.out4_val
    })

    # credit count connections

    connect( s.inctrl_term.out0_credit_cnt, s.outctrl_north.credit_count )
    connect( s.inctrl_term.out1_credit_cnt, s.outctrl_east.credit_count  )
    connect( s.inctrl_term.out2_credit_cnt, s.outctrl_south.credit_count )
    connect( s.inctrl_term.out3_credit_cnt, s.outctrl_west.credit_count  )

    connect( s.inctrl_north.out1_credit_cnt, s.outctrl_east.credit_count )
    connect( s.inctrl_north.out3_credit_cnt, s.outctrl_west.credit_count )

    connect( s.inctrl_south.out1_credit_cnt, s.outctrl_east.credit_count )
    connect( s.inctrl_south.out3_credit_cnt, s.outctrl_west.credit_count )

    connect( s.inctrl_east.out0_credit_cnt, s.outctrl_north.credit_count )
    connect( s.inctrl_east.out2_credit_cnt, s.outctrl_south.credit_count )

    connect( s.inctrl_west.out0_credit_cnt, s.outctrl_north.credit_count )
    connect( s.inctrl_west.out2_credit_cnt, s.outctrl_south.credit_count )

    # requests / grants connections

    connect( s.outctrl_north.reqs[0], s.inctrl_north.reqs[0] )
    connect( s.outctrl_north.reqs[1], s.inctrl_east.reqs[0]  )
    connect( s.outctrl_north.reqs[2], s.inctrl_south.reqs[0] )
    connect( s.outctrl_north.reqs[3], s.inctrl_west.reqs[0]  )
    connect( s.outctrl_north.reqs[4], s.inctrl_term.reqs[0]  )

    connect( s.outctrl_east.reqs[0], s.inctrl_north.reqs[1] )
    connect( s.outctrl_east.reqs[1], s.inctrl_east.reqs[1]  )
    connect( s.outctrl_east.reqs[2], s.inctrl_south.reqs[1] )
    connect( s.outctrl_east.reqs[3], s.inctrl_west.reqs[1]  )
    connect( s.outctrl_east.reqs[4], s.inctrl_term.reqs[1]  )

    connect( s.outctrl_south.reqs[0], s.inctrl_north.reqs[2] )
    connect( s.outctrl_south.reqs[1], s.inctrl_east.reqs[2]  )
    connect( s.outctrl_south.reqs[2], s.inctrl_south.reqs[2] )
    connect( s.outctrl_south.reqs[3], s.inctrl_west.reqs[2]  )
    connect( s.outctrl_south.reqs[4], s.inctrl_term.reqs[2]  )

    connect( s.outctrl_west.reqs[0], s.inctrl_north.reqs[3] )
    connect( s.outctrl_west.reqs[1], s.inctrl_east.reqs[3]  )
    connect( s.outctrl_west.reqs[2], s.inctrl_south.reqs[3] )
    connect( s.outctrl_west.reqs[3], s.inctrl_west.reqs[3]  )
    connect( s.outctrl_west.reqs[4], s.inctrl_term.reqs[3]  )

    connect( s.outctrl_term.reqs[0], s.inctrl_north.reqs[4] )
    connect( s.outctrl_term.reqs[1], s.inctrl_east.reqs[4]  )
    connect( s.outctrl_term.reqs[2], s.inctrl_south.reqs[4] )
    connect( s.outctrl_term.reqs[3], s.inctrl_west.reqs[4]  )
    connect( s.outctrl_term.reqs[4], s.inctrl_term.reqs[4]  )

    connect( s.inctrl_north.grants[0], s.outctrl_north.grants[0] )
    connect( s.inctrl_north.grants[1], s.outctrl_east.grants[0]  )
    connect( s.inctrl_north.grants[2], s.outctrl_south.grants[0] )
    connect( s.inctrl_north.grants[3], s.outctrl_west.grants[0]  )
    connect( s.inctrl_north.grants[4], s.outctrl_term.grants[0]  )

    connect( s.inctrl_east.grants[0], s.outctrl_north.grants[1] )
    connect( s.inctrl_east.grants[1], s.outctrl_east.grants[1]  )
    connect( s.inctrl_east.grants[2], s.outctrl_south.grants[1] )
    connect( s.inctrl_east.grants[3], s.outctrl_west.grants[1]  )
    connect( s.inctrl_east.grants[4], s.outctrl_term.grants[1]  )

    connect( s.inctrl_south.grants[0], s.outctrl_north.grants[2] )
    connect( s.inctrl_south.grants[1], s.outctrl_east.grants[2]  )
    connect( s.inctrl_south.grants[2], s.outctrl_south.grants[2] )
    connect( s.inctrl_south.grants[3], s.outctrl_west.grants[2]  )
    connect( s.inctrl_south.grants[4], s.outctrl_term.grants[2]  )

    connect( s.inctrl_west.grants[0], s.outctrl_north.grants[3] )
    connect( s.inctrl_west.grants[1], s.outctrl_east.grants[3]  )
    connect( s.inctrl_west.grants[2], s.outctrl_south.grants[3] )
    connect( s.inctrl_west.grants[3], s.outctrl_west.grants[3]  )
    connect( s.inctrl_west.grants[4], s.outctrl_term.grants[3]  )

    connect( s.inctrl_term.grants[0], s.outctrl_north.grants[4] )
    connect( s.inctrl_term.grants[1], s.outctrl_east.grants[4]  )
    connect( s.inctrl_term.grants[2], s.outctrl_south.grants[4] )
    connect( s.inctrl_term.grants[3], s.outctrl_west.grants[4]  )
    connect( s.inctrl_term.grants[4], s.outctrl_term.grants[4]  )

class TorusRouterDpath (Model):

  @capture_args
  def __init__( s, router_x_id, router_y_id, num_routers, num_messages, payload_nbits, num_entries ):

    # Local Parameters
    s.netmsg_params = NetMsgParams( num_routers, num_messages, payload_nbits )

    #---------------------------------------------------------------------
    # Interface Ports
    #---------------------------------------------------------------------

    # Port 0 - North

    s.in0_enq_msg   = InPort  ( s.netmsg_params.nbits )
    s.in0_enq_val   = InPort  ( 1 )

    s.in0_dest      = OutPort ( s.netmsg_params.srcdest_nbits )
    s.in0_deq_val   = OutPort ( 1 )
    s.in0_deq_rdy   = InPort  ( 1 )

    s.xbar_sel0     = InPort  ( 3 )
    s.out0_enq_val  = InPort  ( 1 )
    s.out0_deq_msg  = OutPort ( s.netmsg_params.nbits )
    s.out0_deq_val  = OutPort ( 1 )

    # Port 1 - East

    s.in1_enq_msg   = InPort  ( s.netmsg_params.nbits )
    s.in1_enq_val   = InPort  ( 1 )

    s.in1_dest      = OutPort ( s.netmsg_params.srcdest_nbits )
    s.in1_deq_val   = OutPort ( 1 )
    s.in1_deq_rdy   = InPort  ( 1 )

    s.xbar_sel1     = InPort  ( 3 )
    s.out1_enq_val  = InPort  ( 1 )
    s.out1_deq_msg  = OutPort ( s.netmsg_params.nbits )
    s.out1_deq_val  = OutPort ( 1 )

    # Port 2 - South

    s.in2_enq_msg   = InPort  ( s.netmsg_params.nbits )
    s.in2_enq_val   = InPort  ( 1 )

    s.in2_dest      = OutPort ( s.netmsg_params.srcdest_nbits )
    s.in2_deq_val   = OutPort ( 1 )
    s.in2_deq_rdy   = InPort  ( 1 )

    s.xbar_sel2     = InPort  ( 3 )
    s.out2_enq_val  = InPort  ( 1 )
    s.out2_deq_msg  = OutPort ( s.netmsg_params.nbits )
    s.out2_deq_val  = OutPort ( 1 )

    # Port 3 - West

    s.in3_enq_msg   = InPort  ( s.netmsg_params.nbits )
    s.in3_enq_val   = InPort  ( 1 )

    s.in3_dest      = OutPort ( s.netmsg_params.srcdest_nbits )
    s.in3_deq_val   = OutPort ( 1 )
    s.in3_deq_rdy   = InPort  ( 1 )

    s.xbar_sel3     = InPort  ( 3 )
    s.out3_enq_val  = InPort  ( 1 )
    s.out3_deq_msg  = OutPort ( s.netmsg_params.nbits )
    s.out3_deq_val  = OutPort ( 1 )

    # Port 4 - Terminal

    s.in4_enq_msg   = InPort  ( s.netmsg_params.nbits )
    s.in4_enq_val   = InPort  ( 1 )

    s.in4_dest      = OutPort ( s.netmsg_params.srcdest_nbits )
    s.in4_deq_val   = OutPort ( 1 )
    s.in4_deq_rdy   = InPort  ( 1 )

    s.xbar_sel4     = InPort  ( 3 )
    s.out4_enq_val  = InPort  ( 1 )
    s.out4_deq_msg  = OutPort ( s.netmsg_params.nbits )
    s.out4_deq_val  = OutPort ( 1 )

    #---------------------------------------------------------------------
    # Static elaboration
    #---------------------------------------------------------------------

    # Input Queues

    # north
    s.in0_queue = m = NormalQueue( nbits= s.netmsg_params.nbits )
    connect({
      m.enq_bits         : s.in0_enq_msg,
      m.enq_val          : s.in0_enq_val,
      m.deq_val          : s.in0_deq_val,
      m.deq_rdy          : s.in0_deq_rdy
    })

    connect( s.in0_queue.deq_bits[ s.netmsg_params.dest_slice ], s.in0_dest )

    # east
    s.in1_queue = m = NormalQueue( nbits=s.netmsg_params.nbits )
    connect({
      m.enq_bits         : s.in1_enq_msg,
      m.enq_val          : s.in1_enq_val,
      m.deq_val          : s.in1_deq_val,
      m.deq_rdy          : s.in1_deq_rdy
    })

    connect( s.in1_queue.deq_bits[ s.netmsg_params.dest_slice ], s.in1_dest )

    # south
    s.in2_queue = m = NormalQueue( nbits=s.netmsg_params.nbits )
    connect({
      m.enq_bits         : s.in2_enq_msg,
      m.enq_val          : s.in2_enq_val,
      m.deq_val          : s.in2_deq_val,
      m.deq_rdy          : s.in2_deq_rdy
    })

    connect( s.in2_queue.deq_bits[ s.netmsg_params.dest_slice ], s.in2_dest )

    # west
    s.in3_queue = m = NormalQueue( nbits= s.netmsg_params.nbits )
    connect({
      m.enq_bits         : s.in3_enq_msg,
      m.enq_val          : s.in3_enq_val,
      m.deq_val          : s.in3_deq_val,
      m.deq_rdy          : s.in3_deq_rdy
    })

    connect( s.in3_queue.deq_bits[ s.netmsg_params.dest_slice ], s.in3_dest )

    # terminal
    s.in4_queue = m = NormalQueue( nbits=s.netmsg_params.nbits )
    connect({
      m.enq_bits         : s.in4_enq_msg,
      m.enq_val          : s.in4_enq_val,
      m.deq_val          : s.in4_deq_val,
      m.deq_rdy          : s.in4_deq_rdy
    })

    connect( s.in4_queue.deq_bits[ s.netmsg_params.dest_slice ], s.in4_dest )

    # Crossbar

    s.crossbar = m = Crossbar5( router_x_id, router_y_id, nbits=s.netmsg_params.nbits )
    connect({
      m.in0 : s.in0_queue.deq_bits,
      m.sel0 : s.xbar_sel0,
      m.in1 : s.in1_queue.deq_bits,
      m.sel1 : s.xbar_sel1,
      m.in2 : s.in2_queue.deq_bits,
      m.sel2 : s.xbar_sel2,
      m.in3 : s.in3_queue.deq_bits,
      m.sel3 : s.xbar_sel3,
      m.in4 : s.in4_queue.deq_bits,
      m.sel4 : s.xbar_sel4,
    })

    # Channel piped queues

    # north
    s.out0_q = m = SingleElementPipelinedQueue( s.netmsg_params.nbits )
    connect({
      m.enq_bits : s.crossbar.out0,
      m.enq_val  : s.out0_enq_val,
      m.deq_bits : s.out0_deq_msg,
      m.deq_val  : s.out0_deq_val,
      m.deq_rdy  : 1
    })

    # east
    s.out1_q = m = SingleElementPipelinedQueue( s.netmsg_params.nbits )
    connect({
      m.enq_bits : s.crossbar.out1,
      m.enq_val  : s.out1_enq_val,
      m.deq_bits : s.out1_deq_msg,
      m.deq_val  : s.out1_deq_val,
      m.deq_rdy  : 1
    })

    # south
    s.out2_q = m = SingleElementPipelinedQueue( s.netmsg_params.nbits )
    connect({
      m.enq_bits : s.crossbar.out2,
      m.enq_val  : s.out2_enq_val,
      m.deq_bits : s.out2_deq_msg,
      m.deq_val  : s.out2_deq_val,
      m.deq_rdy  : 1
    })

    # west
    s.out3_q = m = SingleElementPipelinedQueue( s.netmsg_params.nbits )
    connect({
      m.enq_bits : s.crossbar.out3,
      m.enq_val  : s.out3_enq_val,
      m.deq_bits : s.out3_deq_msg,
      m.deq_val  : s.out3_deq_val,
      m.deq_rdy  : 1
    })

    # term
    s.out4_q = m = SingleElementPipelinedQueue( s.netmsg_params.nbits )
    connect({
      m.enq_bits : s.crossbar.out4,
      m.enq_val  : s.out4_enq_val,
      m.deq_bits : s.out4_deq_msg,
      m.deq_val  : s.out4_deq_val,
      m.deq_rdy  : 1
    })

class TorusRouter (Model):

  @capture_args
  def __init__( s, router_x_id, router_y_id, num_routers, num_messages, payload_nbits, num_entries ):

    # Local Parameters

    s.netmsg_params = NetMsgParams( num_routers, num_messages, payload_nbits )

    #---------------------------------------------------------------------
    # Interface Ports
    #---------------------------------------------------------------------

    s.in_msg     = [ InPort  ( s.netmsg_params.nbits ) for x in xrange(5) ]
    s.in_val     = [ InPort  ( 1 ) for x in xrange(5) ]
    s.in_credit  = [ OutPort ( 1 ) for x in xrange(5) ]
    s.out_credit = [ InPort  ( 1 ) for x in xrange(5) ]
    s.out_msg    = [ OutPort ( s.netmsg_params.nbits ) for x in xrange(5) ]
    s.out_val    = [ OutPort ( 1 ) for x in xrange(5) ]

    #---------------------------------------------------------------------
    # Static elaboration
    #---------------------------------------------------------------------

    s.ctrl  = TorusRouterCtrl  ( router_x_id, router_y_id, num_routers,
                num_messages, payload_nbits, num_entries )
    s.dpath = TorusRouterDpath ( router_x_id, router_y_id, num_routers,
                num_messages, payload_nbits, num_entries )

    # ctrl unit connections

    connect( s.ctrl.in0_credit,  s.in_credit[0]  )
    connect( s.ctrl.out0_credit, s.out_credit[0] )
    connect( s.ctrl.in1_credit,  s.in_credit[1]  )
    connect( s.ctrl.out1_credit, s.out_credit[1] )
    connect( s.ctrl.in2_credit,  s.in_credit[2]  )
    connect( s.ctrl.out2_credit, s.out_credit[2] )
    connect( s.ctrl.in3_credit,  s.in_credit[3]  )
    connect( s.ctrl.out3_credit, s.out_credit[3] )
    connect( s.ctrl.in4_credit,  s.in_credit[4]  )
    connect( s.ctrl.out4_credit, s.out_credit[4] )

    # dpath unit connections

    connect( s.dpath.in0_enq_msg,  s.in_msg[0]  )
    connect( s.dpath.in0_enq_val,  s.in_val[0]  )
    connect( s.dpath.out0_deq_msg, s.out_msg[0] )
    connect( s.dpath.out0_deq_val, s.out_val[0] )
    connect( s.dpath.in1_enq_msg,  s.in_msg[1]  )
    connect( s.dpath.in1_enq_val,  s.in_val[1]  )
    connect( s.dpath.out1_deq_msg, s.out_msg[1] )
    connect( s.dpath.out1_deq_val, s.out_val[1] )
    connect( s.dpath.in2_enq_msg,  s.in_msg[2]  )
    connect( s.dpath.in2_enq_val,  s.in_val[2]  )
    connect( s.dpath.out2_deq_msg, s.out_msg[2] )
    connect( s.dpath.out2_deq_val, s.out_val[2] )
    connect( s.dpath.in3_enq_msg,  s.in_msg[3]  )
    connect( s.dpath.in3_enq_val,  s.in_val[3]  )
    connect( s.dpath.out3_deq_msg, s.out_msg[3] )
    connect( s.dpath.out3_deq_val, s.out_val[3] )
    connect( s.dpath.in4_enq_msg,  s.in_msg[4]  )
    connect( s.dpath.in4_enq_val,  s.in_val[4]  )
    connect( s.dpath.out4_deq_msg, s.out_msg[4] )
    connect( s.dpath.out4_deq_val, s.out_val[4] )

    # control signal connections (ctrl -> dpath )

    connect( s.ctrl.in0_deq_rdy, s.dpath.in0_deq_rdy  )
    connect( s.ctrl.out0_val,    s.dpath.out0_enq_val )
    connect( s.ctrl.xbar_sel0,   s.dpath.xbar_sel0    )
    connect( s.ctrl.in1_deq_rdy, s.dpath.in1_deq_rdy  )
    connect( s.ctrl.out1_val,    s.dpath.out1_enq_val )
    connect( s.ctrl.xbar_sel1,   s.dpath.xbar_sel1    )
    connect( s.ctrl.in2_deq_rdy, s.dpath.in2_deq_rdy  )
    connect( s.ctrl.out2_val,    s.dpath.out2_enq_val )
    connect( s.ctrl.xbar_sel2,   s.dpath.xbar_sel2    )
    connect( s.ctrl.in3_deq_rdy, s.dpath.in3_deq_rdy  )
    connect( s.ctrl.out3_val,    s.dpath.out3_enq_val )
    connect( s.ctrl.xbar_sel3,   s.dpath.xbar_sel3    )
    connect( s.ctrl.in4_deq_rdy, s.dpath.in4_deq_rdy  )
    connect( s.ctrl.out4_val,    s.dpath.out4_enq_val )
    connect( s.ctrl.xbar_sel4,   s.dpath.xbar_sel4    )

    # status signal connections (ctrl <- dpath)

    connect( s.ctrl.in0_deq_val, s.dpath.in0_deq_val )
    connect( s.ctrl.dest0,       s.dpath.in0_dest    )
    connect( s.ctrl.in1_deq_val, s.dpath.in1_deq_val )
    connect( s.ctrl.dest1,       s.dpath.in1_dest    )
    connect( s.ctrl.in2_deq_val, s.dpath.in2_deq_val )
    connect( s.ctrl.dest2,       s.dpath.in2_dest    )
    connect( s.ctrl.in3_deq_val, s.dpath.in3_deq_val )
    connect( s.ctrl.dest3,       s.dpath.in3_dest    )
    connect( s.ctrl.in4_deq_val, s.dpath.in4_deq_val )
    connect( s.ctrl.dest4,       s.dpath.in4_dest    )