# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/test_controller.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 8640 bytes
import os, sys, unittest, shutil
sys.path.append('.')
from reademptionlib.controller import Controller

class ArgMock(object):
    project_path = 'a_test_project'
    min_read_length = 12
    segemehl_bin = 'segemehl.x'
    threads = 1
    segemehl_accuracy = 95
    segemehl_evalue = 5.0
    paired_end = False
    processes = 1
    check_for_existing_files = False
    poly_a_clipping = True
    progress = False
    split = False
    realign = False
    crossalign_cleaning_str = None
    fastq = False
    min_phred_score = None
    adapter = None
    reverse_complement = False


class TestController(unittest.TestCase):

    def setUp(self):
        arg_mock = ArgMock()
        self.test_project_name = arg_mock.project_path
        self.controller = Controller(arg_mock)
        self.example_data = ExampleData()
        self.maxDiff = None

    def tearDown(self):
        self._remove_project_folder()

    def _generate_input_fasta_files(self):
        genome_fh = open('%s/%s' % (
         self.controller._paths.ref_seq_folder, 'agenome.fa'), 'w')
        read_fh_1 = open('%s/%s' % (
         self.controller._paths.read_fasta_folder, 'libfoo.fa'), 'w')
        read_fh_2 = open('%s/%s' % (
         self.controller._paths.read_fasta_folder, 'libbar.fa'), 'w')
        genome_fh.write(self.example_data.genome_fasta)
        genome_fh.close()
        read_fh_1.write(self.example_data.read_fasta_1)
        read_fh_1.close()
        read_fh_2.write(self.example_data.read_fasta_2)
        read_fh_2.close()

    def _generate_mapping_files(self):
        for file_path, sam_content in zip(self.controller._paths.read_mapping_result_sam_paths, [
         self.example_data.sam_content_1,
         self.example_data.sam_content_2]):
            mapping_fh = open(file_path, 'w')
            mapping_fh.write(sam_content)
            mapping_fh.close()

    def _generate_annotation_files(self):
        annotation_fh = open('%s/some_annos.gff' % self.controller._paths.annotation_folder, 'w')
        print(self.controller._paths.annotation_folder)
        annotation_fh.write(self.example_data.gff_content_1)
        annotation_fh.close()

    def _remove_project_folder(self):
        if os.path.exists(self.test_project_name):
            shutil.rmtree(self.test_project_name)


class TestControllerCreateProject(TestController):

    def test_create_project(self):
        self._version = 0.1
        self.controller.create_project(self._version)
        self.assertEqual(set(list(os.listdir(self.test_project_name))), set(['input', 'output']))
        self._remove_project_folder()


class TestControllerReadAligning(TestController):

    def test_read_aligning(self):
        self._version = 0.1
        self.controller.create_project(self._version)
        self.controller._paths._set_folder_names()
        self._generate_input_fasta_files()
        self.controller.align_reads()
        self._remove_project_folder()


class ExampleData(object):
    genome_fasta = '>SL1344 genome sequence\nAGAGATTACGTCTGGTTGCAAGAGATCATGACAGGGGGAATTGGTTGAAAATAAATATAT\nCGCCAGCAGCACATGAACAAGTTTCGGAATGTGATCAATTTAAAAATTTATTGACTTAGG\nCGGGCAGATACTTTAACCAATATAGGAATACAAGACAGACAAATAAAAATGACAGAGTAC\nACAACATCCATGAACCGCATCAGCACCACCACCATTACCACCATCACCATTACCACAGGT\nAACGGTGCGGGCTGACGCGTACAGGAAACACAGAAAAAAGCCCGCACCTGAACAGTGCGG\nGCTTTTTTTTCGACCAGAGATCACGAGGTAACAACCATGCGAGTGTTGAAGTTCGGCGGT\nACATCAGTGGCAAATGCAGAACGTTTTCTGCGTGTTGCCGATATTCTGGAAAGCAATGCC\nAGGCAAGGGCAGGTAGCGACCGTACTTTCCGCCCCCGCGAAAATTACCAACCATCTGGTG\nGCAATGATTGAAAAAACTATCGGCGGCCAGGATGCTTTGCCGAATATCAGCGATGCAGAA\nCGTATTTTTTCTGACCTGCTCGCAGGACTTGCCAGCGCGCAGCCGGGATTCCCGCTTGCA\nCGGTTGAAAATGGTTGTCGAACAAGAATTCGCTCAGATCAAACATGTTCTGCATGGTATC\nAGCCTGCTGGGTCAGTGCCCGGATAGCATCAACGCCGCGCTGATTTGCCGTGGCGAAAAA\nATGTCGATCGCGATTATGGCGGGACTTCTGGAGGCGCGTGGGCATCGCGTCACGGTGATC\nGATCCGGTAGAAAAATTGCTGGCGGTGGGCCATTACCTTGAATCTACCGTCGATATCGCG\nGAATCGACTCGCCGTATCGCCGCCAGCCAGATCCCGGCCGATCACATGATCCTGATGGCG\nGGCTTTACCGCCGGTAATGAAAAGGGTGAACTGGTGGTGCTGGGCCGTAATGGTTCCGAC\n'
    read_fasta_1 = '>read_01\nAACGGTGCGGGCTGACGCGTACAGGAAACACAGAAAAAAGCCCGCACCTGAACAGTGCGG\n>read_02\nCGGTTGAAAATGGTTGTCGAACAAGAATTCGCTCAGATCAAACATGTTCTGCATGGTATC\n>read_03\nATGTCGATCGCGATTATGGCGGGACTTCTGGAGGCGCGTGGGCATCGCGTCACGGTGATC\n>read_04\nAGGCAAGGGCAGGTAGCGACCGTACTTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n>read_05\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n>read_06\nTTGTCGAACAAGAATTCGCTCAGATCAAAAAAAAAAAAGGGGGTGTAAAAAAAGTGTAAA\n>read_07\nGTGGGGTGGGTAGAGAGAGAGATTTTTTTGAGAGAGAGAAGGGTTTTTAGAGTAGAGAGG\n>read_08\nCGCCAGCCAGATCCCGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n>read_09\nGGCCATTACCTTGAATCTACCGTCGATATCGCGGAATCGACTCGCCGTATCGAAAAAAAA\n>read_10\nAAAGGGACTTCTGGAGGCGCGTGGGCATCGCGTCACGGTGAAAAAAAAAAAAAAAAAAAA\n'
    read_fasta_2 = '>read_01\nTCTGGAGGCGCGTGGGCATCGCGTCACGGTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n>read_02\nGAATCGACTCGCCGTATCGCCGCCAGCCAGATCCCGGCCGATCAGATGATCCTGATGGCG\n>read_03\nATGGCGGGACTTCTGGAGGCGCGTGGGCATCGCGTCACGGTGATCAAAAAAAAAAAAAAA\n>read_04\nGGTCAGTGCCCGGATAGCATCAACGCCGCGCTGATTTGCAAAAAAAAAAAAAAAAAAAAA\n>read_05\nAAGTTTTTTTGTGAGAGAGAAGTTTTGAGAGAGAGTTAGAGGAAAAAAAAAAAAAAAAAA\n>read_06\nCGCCAGCAGCACATGAACAAGTTTCGGAATGTGATCAATTTAAAAATTTATTGACTTAGG\n>read_07\nCGCCAGCAGCACATGAACAAGTTTCGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n>read_08\nATGAACAAGTTTCGGAATGTGATCAATTTAAAAATTTATTGACTTAGGAAAAAAAAAAAA\n>read_09\nTGTGATCAATTTAAAAATTTATTGACTTAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n>read_10\nGGCCATGACCTTGAATCTACCGTCGATATCGCGGAATCGACTCGCCGTATCGAAAAAAAA\n'
    sam_content_1 = '@HD\tVN:1.0\n@SQ\tSN:SL1344\tLN:960\n@PG\tID:segemehl\tVN:0.9.4-$Rev: 316 $ ($Date: 2011-08-18 16:37:19 +0200 (Thu, 18 Aug 2011) $)\nread_01\t0\tSL1344\t1\t255\t10M\t*\t0\t0\tACAACATCCA\t*\tNM:i:0\tMD:Z:10\tNH:i:1\tXA:Z:Q\nread_01\t0\tSL1344\t50\t255\t10M\t*\t0\t0\tACAACATCCA\t*\tNM:i:0\tMD:Z:10\tNH:i:1\tXA:Z:Q\n'
    sam_content_2 = '@HD\tVN:1.0\n@SQ\tSN:SL1344\tLN:960\n@PG\tID:segemehl\tVN:0.9.4-$Rev: 316 $ ($Date: 2011-08-18 16:37:19 +0200 (Thu, 18 Aug 2011) $)\nread_01\t0\tSL1344\t100\t255\t10M\t*\t0\t0\tACAACATCCA\t*\tNM:i:0\tMD:Z:10\tNH:i:1\tXA:Z:Q\nread_01\t0\tSL1344\t500\t255\t10M\t*\t0\t0\tACAACATCCA\t*\tNM:i:0\tMD:Z:10\tNH:i:1\tXA:Z:Q\n'
    gff_content_1 = '##gff-version 3\n#!gff-spec-version 1.14\n#!source-version NCBI C++ formatter 0.2\n##Type DNA SL1344\nSL1344\tEMBL\tgene\t99\t115\t.\t+\t.\tID=SL1344:foo;locus_tag=SL1344_0001\nSL1344\tEMBL\tgene\t99\t115\t.\t-\t.\tID=SL1344:bar;locus_tag=SL1344_0002\nSL1344\tEMBL\tgene\t110\t130\t.\t+\t.\tID=SL1344:samba;locus_tag=SL1344_0003\nSL1344\tEMBL\tgene\t109\t140\t.\t+\t.\tID=SL1344:limbo;locus_tag=SL1344_0004\nSL1344\tEMBL\tgene\t505\t550\t.\t-\t.\tID=SL1344:rumba;locus_tag=SL1344_0005\n'
    gff_content_2 = '##gff-version 3\n#!gff-spec-version 1.14\n#!source-version NCBI C++ formatter 0.2\n##Type DNA SL1344\nSL1344\tEMBL\tsource\t1\t4878012\t.\t+\t.\torganism=Salmonella enterica subsp. enterica serovar Typhimurium str. SL1344;\nSL1344\tEMBL\tgene\t169\t255\t.\t+\t.\tID=SL1344:thrL;locus_tag=SL1344_0001\nSL1344\tEMBL\tCDS\t169\t252\t.\t+\t0\tID=SL1344:thrL:unknown_transcript_1;Parent=SL1344:thrL;locus_tag=SL1344_0001;\nSL1344\tEMBL\tstart_codon\t169\t171\t.\t+\t0\tID=SL1344:thrL:unknown_transcript_1;Parent=SL1344:thrL;locus_tag=SL1344_0001;\nSL1344\tEMBL\tstop_codon\t253\t255\t.\t+\t0\tID=SL1344:thrL:unknown_transcript_1;Parent=SL1344:thrL;locus_tag=SL1344_0001;\nSL1344\tEMBL\tgene\t337\t2799\t.\t+\t.\tID=SL1344:thrA;locus_tag=SL1344_0002\nSL1344\tEMBL\tCDS\t337\t2796\t.\t+\t0\tID=SL1344:thrA:unknown_transcript_1;Parent=SL1344:thrA;locus_tag=SL1344_0002;\nSL1344\tEMBL\tstart_codon\t337\t339\t.\t+\t0\tID=SL1344:thrA:unknown_transcript_1;Parent=SL1344:thrA;locus_tag=SL1344_0002;\nSL1344\tEMBL\tstop_codon\t2797\t2799\t.\t+\t0\tID=SL1344:thrA:unknown_transcript_1;Parent=SL1344:thrA;locus_tag=SL1344_0002;\nSL1344\tEMBL\tmisc_feature\t337\t2796\t.\t+\t.\tID=SL1344:thrA:unknown_transcript_2;Parent=SL1344:thrA;locus_tag=SL1344_0002;\nSL1344\tEMBL\tmisc_feature\t337\t1224\t.\t+\t.\tID=SL1344:thrA:unknown_transcript_3;Parent=SL1344:thrA;locus_tag=SL1344_0002;\nSL1344\tEMBL\tmisc_feature\t349\t351\t.\t+\t.\tID=SL1344:thrA:unknown_transcript_4;Parent=SL1344:thrA;locus_tag=SL1344_0002;\n'
    overlap_output_1 = 'read_01\tSL1344\t100\t109\t+\t1\tSL1344\tEMBL\tgene\t99\t115\t.\t+\t.\tID=SL1344:foo;locus_tag=SL1344_0001\nread_01\tSL1344\t100\t109\t+\t1\tSL1344\tEMBL\tgene\t99\t115\t.\t-\t.\tID=SL1344:bar;locus_tag=SL1344_0002\nread_01\tSL1344\t100\t109\t+\t1\tSL1344\tEMBL\tgene\t109\t140\t.\t+\t.\tID=SL1344:limbo;locus_tag=SL1344_0004\nread_01\tSL1344\t500\t509\t+\t1\tSL1344\tEMBL\tgene\t505\t550\t.\t-\t.\tID=SL1344:rumba;locus_tag=SL1344_0005\n'
    overlap_output_2 = 'read_01\tSL1344\t1\t10\t+\t1\tno_overlap\nread_01\tSL1344\t50\t59\t+\t1\tno_overlap\n'


if __name__ == '__main__':
    unittest.main()