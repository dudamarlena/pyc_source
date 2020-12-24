# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thijs.dezoete/projects/mysql-statsd/mysql_statsd/preprocessors/innodb_preprocessor.py
# Compiled at: 2015-12-16 10:07:10
from interface import Preprocessor
import re

class InnoDBPreprocessor(Preprocessor):
    _INNO_LINE = re.compile('\\s+')
    _DIGIT_LINE = re.compile('\\d+\\.*\\d*')
    tmp_stats = {}
    txn_seen = 0
    prev_line = ''

    @staticmethod
    def increment(stats, value, increment):
        if value in stats:
            stats[value] += increment
        else:
            stats[value] = increment
        return stats

    @staticmethod
    def make_bigint(hi, lo=None):
        if lo == 0:
            return int('0x' + hi, 0)
        else:
            if hi is None:
                hi = 0
            if lo is None:
                lo = 0
            return hi * 4294967296 + lo

    def clear_variables(self):
        self.tmp_stats = {}
        self.txn_seen = 0
        self.prev_line = ''

    def process(self, rows):
        chunks = {'junk': []}
        current_chunk = 'junk'
        next_chunk = False
        oldest_view = False
        self.clear_variables()
        for row in rows:
            innoblob = row[2].replace(',', '').replace(';', '').replace('/s', '').split('\n')
            for line in innoblob:
                if line.startswith('---OLDEST VIEW---'):
                    oldest_view = True
                if line.startswith('----'):
                    if next_chunk == False and oldest_view == False:
                        next_chunk = True
                    else:
                        next_chunk = False
                        oldest_view = False
                elif next_chunk == True:
                    current_chunk = line
                    chunks[current_chunk] = []
                else:
                    chunks[current_chunk].append(line)

        for chunk in chunks:
            if chunk != 'INDIVIDUAL BUFFER POOL INFO':
                for line in chunks[chunk]:
                    self.process_line(line)

        bufferpool = 'bufferpool_0.'
        for line in chunks.get('INDIVIDUAL BUFFER POOL INFO', []):
            if line.startswith('---'):
                innorow = self._INNO_LINE.split(line)
                bufferpool = 'bufferpool_' + innorow[2] + '.'
            else:
                self.process_individual_bufferpools(line, bufferpool)

        return self.tmp_stats.items()

    def process_individual_bufferpools(self, line, bufferpool):
        innorow = self._INNO_LINE.split(line)
        if line.startswith('Buffer pool size ') and not line.startswith('Buffer pool size bytes'):
            self.tmp_stats[bufferpool + 'pool_size'] = innorow[3]
        elif line.startswith('Buffer pool size bytes'):
            self.tmp_stats[bufferpool + 'pool_size_bytes'] = innorow[4]
        elif line.startswith('Free buffers'):
            self.tmp_stats[bufferpool + 'free_pages'] = innorow[2]
        elif line.startswith('Database pages'):
            self.tmp_stats[bufferpool + 'database_pages'] = innorow[2]
        elif line.startswith('Old database pages'):
            self.tmp_stats[bufferpool + 'old_database_pages'] = innorow[3]
        elif line.startswith('Modified db pages'):
            self.tmp_stats[bufferpool + 'modified_pages'] = innorow[3]
        elif line.startswith('Pending reads'):
            self.tmp_stats[bufferpool + 'pending_reads'] = innorow[2]
        elif line.startswith('Pending writes'):
            self.tmp_stats[bufferpool + 'pending_writes_lru'] = self._DIGIT_LINE.findall(innorow[3])[0]
            self.tmp_stats[bufferpool + 'pending_writes_flush_list'] = self._DIGIT_LINE.findall(innorow[6])[0]
            self.tmp_stats[bufferpool + 'pending_writes_single_page'] = innorow[9]
        elif line.startswith('Pages made young'):
            self.tmp_stats[bufferpool + 'pages_made_young'] = innorow[3]
            self.tmp_stats[bufferpool + 'pages_not_young'] = innorow[6]
        elif 'youngs/s' in line:
            self.tmp_stats[bufferpool + 'pages_made_young_ps'] = innorow[0]
            self.tmp_stats[bufferpool + 'pages_not_young_ps'] = innorow[2]
        elif line.startswith('Pages read ahead'):
            self.tmp_stats[bufferpool + 'pages_read_ahead'] = self._DIGIT_LINE.findall(innorow[3])[0]
            self.tmp_stats[bufferpool + 'pages_read_evicted'] = self._DIGIT_LINE.findall(innorow[7])[0]
            self.tmp_stats[bufferpool + 'pages_read_random'] = self._DIGIT_LINE.findall(innorow[11])[0]
        elif line.startswith('Pages read'):
            self.tmp_stats[bufferpool + 'pages_read'] = innorow[2]
            self.tmp_stats[bufferpool + 'pages_created'] = innorow[4]
            self.tmp_stats[bufferpool + 'pages_written'] = innorow[6]
        elif 'reads' in line and 'creates' in line:
            self.tmp_stats[bufferpool + 'pages_read_ps'] = innorow[0]
            self.tmp_stats[bufferpool + 'pages_created_ps'] = innorow[2]
            self.tmp_stats[bufferpool + 'pages_written_ps'] = innorow[4]
        elif line.startswith('Buffer pool hit rate'):
            self.tmp_stats[bufferpool + 'buffer_pool_hit_total'] = self._DIGIT_LINE.findall(innorow[6])[0]
            self.tmp_stats[bufferpool + 'buffer_pool_hits'] = innorow[4]
            self.tmp_stats[bufferpool + 'buffer_pool_young'] = innorow[9]
            self.tmp_stats[bufferpool + 'buffer_pool_not_young'] = innorow[13]
        elif line.startswith('LRU len:'):
            self.tmp_stats[bufferpool + 'lru_len'] = self._DIGIT_LINE.findall(innorow[2])[0]
            self.tmp_stats[bufferpool + 'lru_unzip'] = innorow[5]
        elif line.startswith('I/O sum'):
            self.tmp_stats[bufferpool + 'io_sum'] = self._DIGIT_LINE.findall(innorow[1])[0]
            self.tmp_stats[bufferpool + 'io_sum_cur'] = self._DIGIT_LINE.findall(innorow[1])[1]
            self.tmp_stats[bufferpool + 'io_unzip'] = self._DIGIT_LINE.findall(innorow[3])[0]
            self.tmp_stats[bufferpool + 'io_unzip_cur'] = self._DIGIT_LINE.findall(innorow[3])[0]

    def process_line(self, line):
        innorow = self._INNO_LINE.split(line)
        if line.startswith('Mutex spin waits'):
            self.tmp_stats['spin_waits'] = innorow[3]
            self.tmp_stats['spin_rounds'] = innorow[5]
            self.tmp_stats['os_waits'] = innorow[8]
        elif line.startswith('RW-shared spins') and ';' in line:
            self.tmp_stats['spin_waits'] = innorow[2]
            self.tmp_stats['spin_waits'] = innorow[8]
            self.tmp_stats['os_waits'] = innorow[5]
            self.tmp_stats['os_waits'] += innorow[11]
        elif line.startswith('RW-shared spins') and '; RW-excl spins' in line:
            self.tmp_stats['spin_waits'] = innorow[2]
            self.tmp_stats['os_waits'] = innorow[7]
        elif line.startswith('RW-excl spins'):
            self.tmp_stats['spin_waits'] = innorow[2]
            self.tmp_stats['os_waits'] = innorow[7]
        elif 'seconds the semaphore:' in line:
            self.tmp_stats = self.increment(self.tmp_stats, 'innodb_sem_waits', 1)
            if 'innodb_sem_wait_time_ms' in self.tmp_stats:
                self.tmp_stats['innodb_sem_wait_time_ms'] = float(self.tmp_stats['innodb_sem_wait_time_ms']) + float(innorow[9]) * 1000
            else:
                self.tmp_stats['innodb_sem_wait_time_ms'] = float(innorow[9]) * 1000
        elif line.startswith('Trx id counter'):
            if len(innorow) == 4:
                innorow.append(0)
            self.tmp_stats['innodb_transactions'] = self.make_bigint(innorow[3], innorow[4])
            self.txn_seen = 1
        elif line.startswith('Purge done for trx'):
            if innorow[7] == 'undo':
                innorow[7] = 0
            self.tmp_stats['unpurged_txns'] = int(self.tmp_stats['innodb_transactions']) - self.make_bigint(innorow[6], innorow[7])
        elif line.startswith('History list length'):
            self.tmp_stats['history_list'] = innorow[3]
        elif self.txn_seen == 1 and line.startswith('---TRANSACTION'):
            self.tmp_stats = self.increment(self.tmp_stats, 'current_transactions', 1)
            if 'ACTIVE' in line:
                self.tmp_stats = self.increment(self.tmp_stats, 'active_transactions', 1)
        elif self.txn_seen == 1 and line.startswith('------- TRX HAS BEEN'):
            self.tmp_stats = self.increment(self.tmp_stats, 'innodb_lock_wait_secs', innorow[5])
        elif 'read views open inside InnoDB' in line:
            self.tmp_stats['read_views'] = innorow[0]
        elif line.startswith('mysql tables in use'):
            self.tmp_stats = self.increment(self.tmp_stats, 'innodb_tables_in_use', innorow[4])
            self.tmp_stats = self.increment(self.tmp_stats, 'innodb_locked_tables', innorow[6])
        elif self.txn_seen == 1 and 'lock struct(s)' in line:
            if line.startswith('LOCK WAIT'):
                self.tmp_stats = self.increment(self.tmp_stats, 'innodb_lock_structs', innorow[2])
                self.tmp_stats = self.increment(self.tmp_stats, 'locked_transactions', 1)
            else:
                self.tmp_stats = self.increment(self.tmp_stats, 'innodb_lock_structs', innorow[0])
        elif ' OS file reads, ' in line:
            self.tmp_stats['file_reads'] = innorow[0]
            self.tmp_stats['file_writes'] = innorow[4]
            self.tmp_stats['file_fsyncs'] = innorow[8]
        elif line.startswith('Pending normal aio reads:'):
            self.tmp_stats['pending_normal_aio_reads'] = innorow[4]
            self.tmp_stats['pending_normal_aio_writes'] = innorow[7]
        elif line.startswith('ibuf aio reads'):
            self.tmp_stats['pending_ibuf_aio_reads'] = innorow[3]
            self.tmp_stats['pending_aio_log_ios'] = innorow[6]
            self.tmp_stats['pending_aio_sync_ios'] = innorow[9]
        elif line.startswith('Pending flushes (fsync)'):
            self.tmp_stats['pending_log_flushes'] = innorow[4]
            self.tmp_stats['pending_buf_pool_flushes'] = innorow[7]
        elif line.startswith('Ibuf for space 0: size '):
            self.tmp_stats['ibuf_used_cells'] = innorow[5]
            self.tmp_stats['ibuf_free_cells'] = innorow[9]
            self.tmp_stats['ibuf_cell_count'] = innorow[12]
        elif line.startswith('Ibuf: size '):
            self.tmp_stats['ibuf_used_cells'] = innorow[2]
            self.tmp_stats['ibuf_free_cells'] = innorow[6]
            self.tmp_stats['ibuf_cell_count'] = innorow[9]
            if 'merges' in line:
                self.tmp_stats['ibuf_merges'] = innorow[10]
        elif ', delete mark ' in line and self.prev_line.startswith('merged operations:'):
            self.tmp_stats['ibuf_inserts'] = innorow[1]
            self.tmp_stats['ibuf_merged'] = innorow[1] + innorow[4] + innorow[6]
        elif ' merged recs, ' in line:
            self.tmp_stats['ibuf_inserts'] = innorow[0]
            self.tmp_stats['ibuf_merged'] = innorow[2]
            self.tmp_stats['ibuf_merges'] = innorow[5]
        elif line.startswith('Hash table size '):
            self.tmp_stats['hash_index_cells_total'] = innorow[3]
            if 'used cells' in line:
                self.tmp_stats['hash_index_cells_used'] = innorow[6]
            else:
                self.tmp_stats['hash_index_cells_used'] = 0
        elif " log i/o's done, " in line:
            self.tmp_stats['log_writes'] = innorow[0]
        elif ' pending log writes, ' in line:
            self.tmp_stats['pending_log_writes'] = innorow[0]
            self.tmp_stats['pending_chkp_writes'] = innorow[4]
        elif line.startswith('Log sequence number'):
            if len(innorow) > 4:
                self.tmp_stats['log_bytes_written'] = self.make_bigint(innorow[3], innorow[4])
            else:
                self.tmp_stats['log_bytes_written'] = innorow[3]
        elif line.startswith('Log flushed up to'):
            if len(innorow) > 5:
                self.tmp_stats['log_bytes_flushed'] = self.make_bigint(innorow[4], innorow[5])
            else:
                self.tmp_stats['log_bytes_flushed'] = innorow[4]
        elif line.startswith('Last checkpoint at'):
            if len(innorow) > 4:
                self.tmp_stats['last_checkpoint'] = self.make_bigint(innorow[3], innorow[4])
            else:
                self.tmp_stats['last_checkpoint'] = innorow[3]
        elif line.startswith('Total memory allocated') and 'in additional pool' in line:
            self.tmp_stats['total_mem_alloc'] = innorow[3]
            self.tmp_stats['additional_pool_alloc'] = innorow[8]
        elif line.startswith('Adaptive hash index '):
            self.tmp_stats['adaptive_hash_memory'] = innorow[3]
        elif line.startswith('Page hash           '):
            self.tmp_stats['page_hash_memory'] = innorow[2]
        elif line.startswith('Dictionary cache    '):
            self.tmp_stats['dictionary_cache_memory'] = innorow[2]
        elif line.startswith('File system         '):
            self.tmp_stats['file_system_memory'] = innorow[2]
        elif line.startswith('Lock system         '):
            self.tmp_stats['lock_system_memory'] = innorow[2]
        elif line.startswith('Recovery system     '):
            self.tmp_stats['recovery_system_memory'] = innorow[2]
        elif line.startswith('Threads             '):
            self.tmp_stats['thread_hash_memory'] = innorow[1]
        elif line.startswith('innodb_io_pattern   '):
            self.tmp_stats['innodb_io_pattern_memory'] = innorow[1]
        elif line.startswith('Buffer pool size ') and not line.startswith('Buffer pool size bytes'):
            self.tmp_stats['pool_size'] = innorow[3]
        elif line.startswith('Free buffers'):
            self.tmp_stats['free_pages'] = innorow[2]
        elif line.startswith('Database pages'):
            self.tmp_stats['database_pages'] = innorow[2]
        elif line.startswith('Modified db pages'):
            self.tmp_stats['modified_pages'] = innorow[3]
        elif line.startswith('Pages read ahead'):
            self.tmp_stats['empty'] = ''
        elif line.startswith('Pages read'):
            self.tmp_stats['pages_read'] = innorow[2]
            self.tmp_stats['pages_created'] = innorow[4]
            self.tmp_stats['pages_written'] = innorow[6]
        elif line.startswith('Number of rows inserted'):
            self.tmp_stats['rows_inserted'] = innorow[4]
            self.tmp_stats['rows_updated'] = innorow[6]
            self.tmp_stats['rows_deleted'] = innorow[8]
            self.tmp_stats['rows_read'] = innorow[10]
        elif ' queries inside InnoDB, ' in line:
            self.tmp_stats['queries_inside'] = innorow[0]
            self.tmp_stats['queries_queued'] = innorow[4]