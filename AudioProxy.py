bl_info = {
    "name": "Audio Proxy",
    "category": "Sequencer",
}

import bpy
import os
import ffmpy
import sys


class AudioProxyProperties(bpy.types.PropertyGroup):
    output_path = bpy.props.StringProperty(name="Path", subtype="FILE_PATH", default="//BL_proxy/audio")
    output_format = bpy.props.StringProperty(name="Format", default="ogg")


class AudioProxySequenceProperties(bpy.types.PropertyGroup):
    path_original = bpy.props.StringProperty(name="Original Path", subtype="FILE_PATH")
    path_proxy = bpy.props.StringProperty(name="Proxy Path", subtype="FILE_PATH")


class AudioProxyPanel(bpy.types.Panel):
    bl_idname = "RENDER_PT_audio_proxy"
    bl_label = "Audio Proxy"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        self.layout.label(text="Output Settings:")

        col = layout.column()
        col.prop(scene.audio_proxy,"output_path")
        col.prop(scene.audio_proxy,"output_format")

class AudioProxyUseOrig(bpy.types.Operator):
    bl_idname = "audio_proxy.orig"
    bl_label = "Use Original"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        for s in scene.sequence_editor.sequences:
            if s.type == 'SOUND':
                s.sound.filepath = s.audio_proxy.path_original

        return {'FINISHED'}

class AudioProxyUseProxy(bpy.types.Operator):
    bl_idname = "audio_proxy.proxy"
    bl_label = "Use Proxy"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        for s in scene.sequence_editor.sequences:
            if s.type == 'SOUND':
                s.sound.filepath = s.audio_proxy.path_proxy

        return {'FINISHED'}


class AudioProxyCreate(bpy.types.Operator):
    """Create Proxy Audio Files"""
    bl_idname = "audio_proxy.create"
    bl_label = "Create Audio Proxies"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        for s in scene.sequence_editor.sequences:
            if s.type == 'SOUND':
                path_old=os.path.realpath(bpy.path.abspath(s.sound.filepath))
                path_new=bpy.path.relpath(os.path.join(scene.audio_proxy.output_path,
                    os.path.basename(s.sound.filepath) + "."+scene.audio_proxy.output_format))

                s.audio_proxy.path_original=s.sound.filepath
                s.audio_proxy.path_proxy=path_new

                # Test if channel directory exists
                audio_path=os.path.dirname(bpy.path.abspath(path_new))
                print(audio_path)
                if not os.path.isdir(audio_path):
                    os.makedirs(audio_path)

                # Test if proxy file already made
                if not os.path.isfile(bpy.path.abspath(path_new)):
                    ff = ffmpy.FFmpeg(
                        inputs={path_old: None},
                        outputs={bpy.path.abspath(path_new): ['-vn']}
                    )
                    ff.run()

        return {'FINISHED'}


class AudioProxySubMenu(bpy.types.Menu):
    bl_idname = "AudioProxySubMenu"
    bl_label = "Audio Proxy..."

    def draw(self, context):
        layout = self.layout

        layout.operator(AudioProxyCreate.bl_idname)
        layout.operator(AudioProxyUseOrig.bl_idname)
        layout.operator(AudioProxyUseProxy.bl_idname)



def menu_func(self, context):
    self.layout.menu(AudioProxySubMenu.bl_idname)
    self.layout.separator()

@persistent
def use_orig(self):
    bpy.ops.audio_proxy.orig()

def register():
    bpy.utils.register_class(AudioProxyUseOrig)
    bpy.utils.register_class(AudioProxyUseProxy)
    bpy.utils.register_class(AudioProxyCreate)
    bpy.utils.register_class(AudioProxyPanel)
    bpy.utils.register_class(AudioProxyProperties)
    bpy.utils.register_class(AudioProxySequenceProperties)
    bpy.utils.register_class(AudioProxySubMenu)

    bpy.types.SEQUENCER_MT_strip.prepend(menu_func)

    bpy.types.Scene.audio_proxy = \
        bpy.props.PointerProperty(type=AudioProxyProperties)
    bpy.types.SoundSequence.audio_proxy = \
        bpy.props.PointerProperty(type=AudioProxySequenceProperties)

    bpy.app.handlers.render_pre.append(use_orig)


def unregister():
    bpy.utils.unregister_class(AudioProxyUseOrig)
    bpy.utils.unregister_class(AudioProxyUseProxy)
    bpy.utils.unregister_class(AudioProxyCreate)
    bpy.utils.unregister_class(AudioProxyPanel)
    bpy.utils.unregister_class(AudioProxyProperties)
    bpy.utils.unregister_class(AudioProxySequenceProperties)
    bpy.utils.unregister_class(AudioProxySubMenu)

    bpy.types.SEQUENCER_MT_strip.remove(menu_func)

    del bpy.types.Scene.audio_proxy
    del bpy.types.SoundSequence.audio_proxy


if __name__ == "__main__":
    register()

