# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\GameObject.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 896 bytes
from .EditorExtension import EditorExtension
from .PPtr import PPtr

class GameObject(EditorExtension):
    __doc__ = '\n    public PPtr<Component>[] m_Components;\n    public string m_Name;\n    public Transform m_Transform;\n    public MeshRenderer m_MeshRenderer;\n    public MeshFilter m_MeshFilter;\n    public SkinnedMeshRenderer m_SkinnedMeshRenderer;\n    public Animator m_Animator;\n    public Animation m_Animation;\n    '

    def __init__(self, reader):
        super().__init__(reader=reader)
        component_size = reader.read_int()
        self.components = []
        for i in range(component_size):
            if self.version[0] < 5 or self.version[0] == 5 and self.version[1] < 5:
                first = reader.read_int()
            self.components.append(PPtr(reader))

        self.layer = reader.read_int()
        self.name = reader.read_aligned_string()