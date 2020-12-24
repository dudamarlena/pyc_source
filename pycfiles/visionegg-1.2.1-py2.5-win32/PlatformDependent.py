# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PlatformDependent.py
# Compiled at: 2009-07-07 11:29:42
"""
Implementations of functions which vary by platform.

"""
import logging, sys, os, VisionEgg, VisionEgg.Core, VisionEgg.GL as gl

def set_priority(*args, **kw):
    """Set the priority of the Vision Egg application.

    Defaults to maximum priority, but can be changed via keyword
    arguments.

    Raises an exception on failure.
    """
    parse_me = [
     'darwin_realtime_period_denom',
     'darwin_realtime_computation_denom',
     'darwin_realtime_constraint_denom',
     'darwin_realtime_preemptible',
     'darwin_maxpriority_conventional_not_realtime',
     'darwin_conventional_priority',
     'darwin_pthread_priority']
    logger = logging.getLogger('VisionEgg.PlatformDependent')
    params = {}
    for word in parse_me:
        config_name = 'VISIONEGG_' + word.upper()
        if hasattr(VisionEgg.config, config_name):
            value = getattr(VisionEgg.config, config_name)
        else:
            value = None
        if word in kw.keys():
            value = kw[word]
        if value is not None:
            params[word] = value

    if sys.platform == 'darwin':
        import darwin_maxpriority
        if params['darwin_maxpriority_conventional_not_realtime']:
            process = darwin_maxpriority.PRIO_PROCESS
            policy = darwin_maxpriority.SCHED_RR
            logger.info('Setting max priority mode for darwin platform using conventional priority %d.' % (
             params['darwin_conventional_priority'],))
            darwin_maxpriority.setpriority(process, 0, params['darwin_conventional_priority'])
            darwin_pthread_priority = params['darwin_pthread_priority']
            if darwin_pthread_priority == 'max':
                darwin_pthread_priority = darwin_maxpriority.sched_get_priority_max(policy)
            if darwin_maxpriority.set_self_pthread_priority(policy, darwin_pthread_priority) == -1:
                raise RuntimeError('set_self_pthread failed.')
        else:
            bus_speed = darwin_maxpriority.get_bus_speed()
            logger.info('Setting max priority mode for darwin platform using realtime threads. ( period = %d / %d, computation = %d / %d, constraint = %d / %d, preemptible = %d )' % (
             bus_speed, params['darwin_realtime_period_denom'],
             bus_speed, params['darwin_realtime_computation_denom'],
             bus_speed, params['darwin_realtime_constraint_denom'],
             params['darwin_realtime_preemptible']))
            period = bus_speed / params['darwin_realtime_period_denom']
            computation = bus_speed / params['darwin_realtime_computation_denom']
            constraint = bus_speed / params['darwin_realtime_constraint_denom']
            preemptible = params['darwin_realtime_preemptible']
            darwin_maxpriority.set_self_thread_time_constraint_policy(period, computation, constraint, preemptible)
    elif sys.platform == 'win32':
        import win32_maxpriority
        logger.info("Setting priority for win32 platform to HIGH_PRIORITY_CLASS, THREAD_PRIORITY_HIGHEST. (This is Microsoft's maximum recommended priority, but you could still raise it higher.)")
        win32_maxpriority.set_self_process_priority_class(win32_maxpriority.HIGH_PRIORITY_CLASS)
        win32_maxpriority.set_self_thread_priority(win32_maxpriority.THREAD_PRIORITY_HIGHEST)
    elif sys.platform.startswith('irix') or sys.platform.startswith('linux') or sys.platform.startswith('posix'):
        import posix_maxpriority
        policy = posix_maxpriority.SCHED_FIFO
        max_priority = posix_maxpriority.sched_get_priority_max(policy)
        logger.info('Setting priority for POSIX-compatible platform to policy SCHED_FIFO and priority to %d' % max_priority)
        posix_maxpriority.set_self_policy_priority(policy, max_priority)
        posix_maxpriority.stop_memory_paging()
    else:
        raise RuntimeError("Cannot change priority.  Unknown platform '%s'" % sys.platform)
    return


def linux_but_unknown_drivers():
    """Warn that platform is linux, but drivers not known."""
    logger = logging.getLogger('VisionEgg.PlatformDependent')
    logger.warning('Could not sync buffer swapping to vblank because you are running linux but not known/supported drivers (only nVidia and recent Mesa DRI Radeon currently supported).')


def sync_swap_with_vbl_pre_gl_init():
    """Try to synchronize buffer swapping and vertical retrace before starting OpenGL."""
    success = 0
    if sys.platform.startswith('linux'):
        VisionEgg.Core.add_gl_assumption('__SPECIAL__', 'linux_nvidia_or_new_ATI', linux_but_unknown_drivers)
        os.environ['__GL_SYNC_TO_VBLANK'] = '1'
        os.environ['LIBGL_SYNC_REFRESH'] = '1'
        success = 1
    elif sys.platform.startswith('irix'):
        logger = logging.getLogger('VisionEgg.PlatformDependent')
        logger.info('IRIX platform detected, assuming retrace sync.')
    return success


def sync_swap_with_vbl_post_gl_init():
    """Try to synchronize buffer swapping and vertical retrace after starting OpenGL."""
    success = 0
    try:
        if sys.platform == 'win32':
            import OpenGL.WGL.EXT.swap_control
            if OpenGL.WGL.EXT.swap_control.wglInitSwapControlARB():
                OpenGL.WGL.EXT.swap_control.wglSwapIntervalEXT(1)
                if OpenGL.WGL.EXT.swap_control.wglGetSwapIntervalEXT() == 1:
                    success = 1
        elif sys.platform == 'darwin':
            try:
                import _darwin_sync_swap
                _darwin_sync_swap.sync_swap()
                success = 1
            except Exception, x:
                logger = logging.getLogger('VisionEgg.PlatformDependent')
                logger.warning('Failed trying to synchronize buffer swapping on darwin: %s: %s' % (
                 str(x.__class__), str(x)))

    except:
        pass

    return success


def query_refresh_rate(screen):
    if sys.platform == 'win32':
        import win32_getrefresh
        return win32_getrefresh.getrefresh()
    elif sys.platform == 'darwin':
        import darwin_getrefresh
        return darwin_getrefresh.getrefresh()
    else:
        raise NotImplementedError('Platform dependent code to query frame rate not implemented on this platform.')


def attempt_to_load_multitexturing():
    """Attempt to load multitexturing functions and constants.

    Inserts the results into the gl module, which makes them globally
    available."""
    logger = logging.getLogger('VisionEgg.PlatformDependent')
    try:
        import ctypes
        if sys.platform.startswith('linux'):
            libGL = ctypes.cdll.LoadLibrary('/usr/lib/libGL.so')
        elif sys.platform == 'win32':
            libGL = ctypes.cdll.LoadLibrary('opengl32.dll')
        else:
            raise NotImplementedError('ctypes support not added for this platform')
        libGL.glGetString.restype = ctypes.c_char_p
        vers = libGL.glGetString(ctypes.c_int(gl.GL_VERSION))
        logger.debug('ctypes loaded OpenGL %s' % vers)
        gl.glActiveTexture = libGL.glActiveTexture
        gl.glActiveTexture.argtypes = [ctypes.c_int]
        gl.glMultiTexCoord2f = libGL.glMultiTexCoord2f
        gl.glMultiTexCoord2f.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float]
        gl.GL_TEXTURE0 = 33984
        gl.GL_TEXTURE1 = 33985
        logger.debug('ctypes loaded OpenGL library and multitexture names are present.  Workaround appears successful. ')
    except Exception, x:
        logger.debug('ctypes loading of OpenGL library failed %s: %s' % (
         x.__class__, str(x)))
        if VisionEgg.Core.init_gl_extension('ARB', 'multitexture'):
            gl.glActiveTexture = gl.glActiveTextureARB
            gl.glMultiTexCoord2f = gl.glMultiTexCoord2fARB
            gl.GL_TEXTURE0 = gl.GL_TEXTURE0_ARB
            gl.GL_TEXTURE1 = gl.GL_TEXTURE1_ARB
            logger.debug('loaded multitexturing ARB extension')
        else:
            logger.warning('multitexturing not available after trying ctypes and the OpenGL ARB extension. Some features will not be available')