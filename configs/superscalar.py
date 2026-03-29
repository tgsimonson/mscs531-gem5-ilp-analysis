import m5
from m5.objects import *

# Superscalar experiment: O3CPU with 4-wide issue
# Increases instructions issued per cycle vs single-issue baseline

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

system.cpu = DerivO3CPU()
system.cpu.issueWidth = 4
system.cpu.decodeWidth = 4
system.cpu.fetchWidth = 4
system.cpu.commitWidth = 4
system.cpu.dispatchWidth = 4
system.cpu.renameWidth = 4
system.cpu.branchPred = BranchPredictor(
    conditionalBranchPred=TournamentBP(numThreads=1)
)

system.membus = SystemXBar()

system.cpu.icache = Cache(
    size="32kB",
    assoc=4,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20
)

system.cpu.dcache = Cache(
    size="32kB",
    assoc=4,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=20
)

system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible("benchmarks/matrix_multiply")
process = Process()
process.cmd = ["benchmarks/matrix_multiply"]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause()))