# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/samples/sample_kclpy_app.py
# Compiled at: 2016-07-11 11:35:21
__doc__ = '\nCopyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.\n\nLicensed under the Amazon Software License (the "License").\nYou may not use this file except in compliance with the License.\nA copy of the License is located at\n\nhttp://aws.amazon.com/asl/\n\nor in the "license" file accompanying this file. This file is distributed\non an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either\nexpress or implied. See the License for the specific language governing\npermissions and limitations under the License.\n'
from __future__ import print_function
import sys, time, json, base64
from amazon_kclpy import kcl

class RecordProcessor(kcl.RecordProcessorBase):
    """
    A RecordProcessor processes a shard in a stream. Its methods will be called with this pattern:

    - initialize will be called once
    - process_records will be called zero or more times
    - shutdown will be called if this MultiLangDaemon instance loses the lease to this shard
    """

    def __init__(self):
        self.SLEEP_SECONDS = 5
        self.CHECKPOINT_RETRIES = 5
        self.CHECKPOINT_FREQ_SECONDS = 60

    def initialize(self, shard_id):
        """
        Called once by a KCLProcess before any calls to process_records

        :type shard_id: str
        :param shard_id: The shard id that this processor is going to be working on.
        """
        self.largest_seq = None
        self.last_checkpoint_time = time.time()
        return

    def checkpoint(self, checkpointer, sequence_number=None):
        """
        Checkpoints with retries on retryable exceptions.

        :type checkpointer: amazon_kclpy.kcl.Checkpointer
        :param checkpointer: A checkpointer provided to either process_records or shutdown

        :type sequence_number: str
        :param sequence_number: A sequence number to checkpoint at.
        """
        for n in range(0, self.CHECKPOINT_RETRIES):
            try:
                checkpointer.checkpoint(sequence_number)
                return
            except kcl.CheckpointError as e:
                if 'ShutdownException' == e.value:
                    print('Encountered shutdown execption, skipping checkpoint')
                    return
                if 'ThrottlingException' == e.value:
                    if self.CHECKPOINT_RETRIES - 1 == n:
                        sys.stderr.write(('Failed to checkpoint after {n} attempts, giving up.\n').format(n=n))
                        return
                    print(('Was throttled while checkpointing, will attempt again in {s} seconds').format(s=self.SLEEP_SECONDS))
                elif 'InvalidStateException' == e.value:
                    sys.stderr.write('MultiLangDaemon reported an invalid state while checkpointing.\n')
                else:
                    sys.stderr.write(('Encountered an error while checkpointing, error was {e}.\n').format(e=e))

            time.sleep(self.SLEEP_SECONDS)

    def process_record(self, data, partition_key, sequence_number):
        """
        Called for each record that is passed to process_records.

        :type data: str
        :param data: The blob of data that was contained in the record.

        :type partition_key: str
        :param partition_key: The key associated with this recod.

        :type sequence_number: int
        :param sequence_number: The sequence number associated with this record.
        """
        message = ('Received: p:{pk}, s:{sn}, d:{data}').format(pk=partition_key, sn=sequence_number, data=data)
        sys.stdout.write(message)

    def process_records(self, records, checkpointer):
        """
        Called by a KCLProcess with a list of records to be processed and a checkpointer which accepts sequence numbers
        from the records to indicate where in the stream to checkpoint.

        :type records: list
        :param records: A list of records that are to be processed. A record looks like
            {"data":"<base64 encoded string>","partitionKey":"someKey","sequenceNumber":"1234567890"} Note that "data" is a base64
            encoded string. You can use base64.b64decode to decode the data into a string. We currently do not do this decoding for you
            so as to leave it to your discretion whether you need to decode this particular piece of data.

        :type checkpointer: amazon_kclpy.kcl.Checkpointer
        :param checkpointer: A checkpointer which accepts a sequence number or no parameters.
        """
        try:
            for record in records:
                data = base64.b64decode(record.get('data'))
                seq = record.get('sequenceNumber')
                seq = int(seq)
                key = record.get('partitionKey')
                self.process_record(data, key, seq)
                if self.largest_seq == None or seq > self.largest_seq:
                    self.largest_seq = seq

            if time.time() - self.last_checkpoint_time > self.CHECKPOINT_FREQ_SECONDS:
                self.checkpoint(checkpointer, str(self.largest_seq))
                self.last_checkpoint_time = time.time()
        except Exception as e:
            sys.stderr.write(('Encountered an exception while processing records. Exception was {e}\n').format(e=e))

        return

    def shutdown(self, checkpointer, reason):
        """
        Called by a KCLProcess instance to indicate that this record processor should shutdown. After this is called,
        there will be no more calls to any other methods of this record processor.

        :type checkpointer: amazon_kclpy.kcl.Checkpointer
        :param checkpointer: A checkpointer which accepts a sequence number or no parameters.

        :type reason: str
        :param reason: The reason this record processor is being shutdown, either TERMINATE or ZOMBIE. If ZOMBIE,
            clients should not checkpoint because there is possibly another record processor which has acquired the lease
            for this shard. If TERMINATE then checkpointer.checkpoint() should be called to checkpoint at the end of the
            shard so that this processor will be shutdown and new processor(s) will be created to for the child(ren) of
            this shard.
        """
        try:
            if reason == 'TERMINATE':
                print('Was told to terminate, will attempt to checkpoint.')
                self.checkpoint(checkpointer, None)
            else:
                print('Shutting down due to failover. Will not checkpoint.')
        except:
            pass

        return


if __name__ == '__main__':
    kclprocess = kcl.KCLProcess(RecordProcessor())
    kclprocess.run()