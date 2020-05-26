# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:30:25 2020

@author: Weirroswei
"""


#来源库，支持多个，B64


DbS = b'CidFT1BDRTgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjEwMC42OjE0MzMvRU9QQ0U4MDAnCiwnRU9QUlQ4ODAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMDAuNjoxNDMzL0VPUFJUODgwJwosJ0VPUFdYODAwJzonbXNzcWwrcHltc3NxbDovL3NhOkNvbXBhc3MyMDA4QDE5Mi4xNjguMTAwLjY6MTQzMy9FT1BXWDgwMCcKLCdFT1BZTDgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjEwMC42OjE0MzMvRU9QWUw4MDAnCiwnRU9QRVQ4MDAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMTguODU6MTQzMy9FT1BFVDgwMCcKLCdFT1BHTDgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjExOC44NToxNDMzL0VPUEdMODAwJwosJ0VPUEpZODAwJzonbXNzcWwrcHltc3NxbDovL3NhOkNvbXBhc3MyMDA4QDE5Mi4xNjguMTE4Ljg1OjE0MzMvRU9QSlk4MDAnCiwnRU9QS0g4MDAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMTguODU6MTQzMy9FT1BLSDgwMCcKLCdFT1BPUDgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjExOC44NToxNDMzL0VPUE9QODAwJwosJ0VPUFJYODAwJzonbXNzcWwrcHltc3NxbDovL3NhOkNvbXBhc3MyMDA4QDE5Mi4xNjguMTE4Ljg1OjE0MzMvRU9QUlg4MDAnCiwnRU9QU0g4MDAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMTguODU6MTQzMy9FT1BTSDgwMCcKLCdFT1BTSjgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjExOC44NToxNDMzL0VPUFNKODAwJwoKLCdFT1BIUTgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjExOC44NjoxNDMzL0VPUEhRODAwJwosJ0VPUExaODAwJzonbXNzcWwrcHltc3NxbDovL3NhOkNvbXBhc3MyMDA4QDE5Mi4xNjguMTE4Ljg2OjE0MzMvRU9QTFo4MDAnCiwnRU9QUlk4MDAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMTguODY6MTQzMy9FT1BSWTgwMCcKCiwnRU9QQ1o4MDAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMTguODc6MTQzMy9FT1BDWjgwMCcKLCdFT1BEVDgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjExOC44NzoxNDMzL0VPUERUODAwJwosJ0VPUEpTODAwJzonbXNzcWwrcHltc3NxbDovL3NhOkNvbXBhc3MyMDA4QDE5Mi4xNjguMTE4Ljg3OjE0MzMvRU9QSlM4MDAnCiwnRU9QSlc4MDAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMTguODc6MTQzMy9FT1BKVzgwMCcKLCdFT1BCRTgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjExOC44ODoxNDMzL0VPUEJFODAwJwosJ0VPUEJKODAwJzonbXNzcWwrcHltc3NxbDovL3NhOkNvbXBhc3MyMDA4QDE5Mi4xNjguMTE4Ljg4OjE0MzMvRU9QQko4MDAnCiwnRU9QSFQ4MDAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMTguODg6MTQzMy9FT1BIVDgwMCcKLCdFT1BHWTgwMCc6J21zc3FsK3B5bXNzcWw6Ly9zYTpDb21wYXNzMjAwOEAxOTIuMTY4LjEzOS44NToxNDMzL0VPUEdZODAwJwosJ0VPUEdaODAwJzonbXNzcWwrcHltc3NxbDovL3NhOkNvbXBhc3MyMDA4QDE5Mi4xNjguMTM5Ljg1OjE0MzMvRU9QR1o4MDAnCiwnRU9QSFM4MDAnOidtc3NxbCtweW1zc3FsOi8vc2E6Q29tcGFzczIwMDhAMTkyLjE2OC4xMzkuODU6MTQzMy9FT1BIUzgwMCcKCg=='

