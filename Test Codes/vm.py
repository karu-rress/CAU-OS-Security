from optparse import OptionParser
import random
import math

## Constant Configuration
PAGE_SIZE = '2k'
VIRTUAL_MEMORY_SIZE = '16k'
PHYSICAL_MEMORY_SIZE = '128k'

def check_power_of_2(bits, size, msg):
    if math.pow(2, bits) != size:
        raise Exception(f'Error in argument: {msg}')

def check_multiple_of(bignum, num, msg):
    if int(float(bignum) / float(num)) != (int(bignum) / int(num)):
        raise Exception(f'Error in argument: {msg}')

# Converts to bytes
def convert(size):
    lastchar = size[-1]
    if lastchar in ['k', 'K']: # kilobytes
        m = 1024
        nsize = int(size[:-1]) * m
    elif lastchar in ['m', 'M']: # megabytes
        m = 1024*1024
        nsize = int(size[:-1]) * m
    elif lastchar in ['g', 'G']: # gigabytes
        m = 1024*1024*1024
        nsize = int(size[:-1]) * m
    else:
        nsize = int(size)

    return nsize


if __name__ == '__main__':
    random.seed(42)

    vms_size = convert(VIRTUAL_MEMORY_SIZE)
    pms_size = convert(PHYSICAL_MEMORY_SIZE)
    page_size = convert(PAGE_SIZE)

    # Asserts
    assert pms_size > 1, "Error: must specify a non-zero physical memory size."
    assert vms_size > 1, "Error: must specify a non-zero address-space size."
    assert pms_size > vms_size, "Error: physical memory size must be GREATER than address space size (for this simulation)"
    assert pms_size < convert('1g') and vms_size < convert('1g'), "Error: must use smaller sizes (less than 1 GB) for this simulation."
    check_multiple_of(vms_size, page_size, 'address space must be a multiple of the pagesize')
    check_multiple_of(pms_size, page_size, 'physical memory must be a multiple of the pagesize')

    # print some useful info, like the darn page table
    pages = int(pms_size / page_size)

    used = []
    pt = []

    for i in range(0, pages):
        used.insert(i, 0)

    vpages = int(vms_size / page_size)

    # now, assign some pages of the VA
    vms_bits = int(math.log(float(vms_size)) / math.log(2.0))
    check_power_of_2(vms_bits, vms_size, 'address space must be a power of 2')

    page_bits = int(math.log(float(page_size)) / math.log(2.0))
    check_power_of_2(page_bits, page_size, 'page size must be a power of 2')

    vpnbits = vms_bits - page_bits
    pagemask = (1 << page_bits) - 1

    # import ctypes
    # vpnmask  = ctypes.c_uint32(~pagemask).value
    vpnmask = 0xFFFFFFFF & ~pagemask

    #if vpnmask2 != vpnmask:
    #    print 'ERROR'
    #    exit(1)
    # print 'va:%d page:%d vpn:%d -- %08x %08x' % (vabits, pagebits, vpnbits, vpnmask, pagemask)

    print()
    print('The format of the page table is simple:')
    print('The high-order (left-most) bit is the VALID bit.')
    print('  If the bit is 1, the rest of the entry is the PFN.')
    print('  If the bit is 0, the page is not valid.')
    print('Use verbose mode (-v) if you want to print the VPN # by')
    print('each entry of the page table.')
    print()

    parser = OptionParser()
    parser.add_option("-n", "--num", default=10, help="Number of virtual addresses to generate (default is 10)", action="store", type="int", dest="num")
    parser.add_option("-a", "--addresses", default="-1", help="Instead of generating random addresses, use the comma-separated list of virtual addresses supplied on the command line.", action="store", type="string", dest="addresses")
    parser.add_option("-v", "--verbose", help="Print out lots of info (e.g., the VPN for each entry in the page table)", action="store_true", default=False, dest="verbose")
    parser.add_option("-s", "--solve", help="Solve the translations as well, to check your answers.", action="store_true", default=False, dest="solve")
    parser.add_option("-u", "--used", default=100, help="Set the percentage of physical memory that is used/mapped (default is 100).", action="store", type="int", dest="used")

    options, args = parser.parse_args()
    addresses = options.addresses

    print('Page Table (from entry 0 down to the max size)')
    for v in range(0,vpages):
        done = 0
        while done == 0:
            if ((random.random() * 100.0) > (100.0 - float(options.used))):
                u = int(pages * random.random())
                if used[u] == 0:
                    used[u] = 1
                    done = 1
                    # print('%8d - %d' % (v, u))
                    if options.verbose == True:
                        print('  [%8d]  ' % v, end='')
                    else:
                        print('  ', end='')
                    print(f'0x{(0x80000000 | u):08x}')
                    pt.insert(v,u)
            else:
                # print('%8d - not valid' % v)
                if options.verbose == True:
                    print(f'  [{v:8d}]  ', end='')
                else:
                    print('  ', end='')
                print(f'0x{0:08x}')
                pt.insert(v,-1)
                done = 1
    print()

    #
    # now, need to generate virtual address trace
    #

    addrList = []
    if addresses == '-1':
        # need to generate addresses
        for i in range(0, options.num):
            n = int(vms_size * random.random())
            addrList.append(n)
    else:
        addrList = addresses.split(',')

    print('Virtual Address Trace')
    for vStr in addrList:
        # vaddr = int(asize * random.random())
        vaddr = int(vStr)
        if options.solve == False:
            print(f'  VA 0x{vaddr:08x} (decimal: {vaddr:8d}) --> PA or invalid address?')
        else:
            paddr = 0
            # split vaddr into VPN | offset
            vpn = (vaddr & vpnmask) >> page_bits
            if pt[vpn] < 0:
                print(f'  VA 0x{vaddr:08x} (decimal: {vaddr:8d}) --> Invalid (VPN {vpn} not valid)')
            else:
                pfn    = pt[vpn]
                offset = vaddr & pagemask
                paddr  = (pfn << page_bits) | offset
                print(f'  VA 0x{vaddr:08x} (decimal: {vaddr:8d}) --> 0x{paddr:08x} (decimal {paddr:8d}) [VPN {vpn}]')
    print()

    if options.solve == False:
        print('For each virtual address, write down the physical address it translates to')
        print('OR write down that it is an out-of-bounds address (e.g., segfault).')
        print()