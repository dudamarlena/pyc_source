# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/shwirl/shaders/render_volume.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 46819 bytes
from __future__ import division
from extern.vispy.gloo import Texture3D, TextureEmulated3D, VertexBuffer, IndexBuffer
from extern.vispy.visuals import Visual
from extern.vispy.visuals.shaders import Function
from extern.vispy.color import get_colormap
from extern.vispy.scene.visuals import create_visual_node
from extern.vispy.io import load_spatial_filters
import numpy as np
VERT_SHADER = '\nattribute vec3 a_position;\n// attribute vec3 a_texcoord;\nuniform vec3 u_shape;\n\n// varying vec3 v_texcoord;\nvarying vec3 v_position;\nvarying vec4 v_nearpos;\nvarying vec4 v_farpos;\n\nvoid main() {\n    // v_texcoord = a_texcoord;\n    v_position = a_position;\n\n    // Project local vertex coordinate to camera position. Then do a step\n    // backward (in cam coords) and project back. Voila, we get our ray vector.\n    vec4 pos_in_cam = $viewtransformf(vec4(v_position, 1));\n\n    // intersection of ray and near clipping plane (z = -1 in clip coords)\n    pos_in_cam.z = -pos_in_cam.w;\n    v_nearpos = $viewtransformi(pos_in_cam);\n\n    // intersection of ray and far clipping plane (z = +1 in clip coords)\n    pos_in_cam.z = pos_in_cam.w;\n    v_farpos = $viewtransformi(pos_in_cam);\n\n    gl_Position = $transform(vec4(v_position, 1.0));\n}\n'
FRAG_SHADER = "\n// uniforms\nuniform $sampler_type u_volumetex;\nuniform vec3 u_shape;\nuniform vec3 u_resolution;\nuniform float u_threshold;\nuniform float u_relative_step_size;\n//uniform int u_color_scale;\n//uniform float u_data_min;\n//uniform float u_data_max;\n\n// Moving box filter variables\nuniform int u_filter_size;\nuniform float u_filter_coeff;\nuniform int u_filter_arm;\nuniform int u_filter_type;\n\nuniform int u_use_gaussian_filter;\nuniform int u_gaussian_filter_size;\n\n//uniform int u_log_scale;\n\n// Volume Stats\n//uniform float u_volume_mean;\n//uniform float u_volume_std;\n//uniform float u_volume_madfm;\nuniform float u_high_discard_filter_value;\nuniform float u_low_discard_filter_value;\nuniform float u_density_factor;\n\nuniform int u_color_method;\n\n//varyings\n// varying vec3 v_texcoord;\nvarying vec3 v_position;\nvarying vec4 v_nearpos;\nvarying vec4 v_farpos;\n\n// uniforms for lighting. Hard coded until we figure out how to do lights\nconst vec4 u_ambient = vec4(0.2, 0.4, 0.2, 1.0);\nconst vec4 u_diffuse = vec4(0.8, 0.2, 0.2, 1.0);\nconst vec4 u_specular = vec4(1.0, 1.0, 1.0, 1.0);\nconst float u_shininess = 40.0;\n\n//varying vec3 lightDirs[1];\n\n// global holding view direction in local coordinates\nvec3 view_ray;\n\nfloat rand(vec2 co)\n{{\n    // Create a pseudo-random number between 0 and 1.\n    // http://stackoverflow.com/questions/4200224\n    return fract(sin(dot(co.xy ,vec2(12.9898, 78.233))) * 43758.5453);\n}}\n\nfloat colorToVal(vec4 color1)\n{{\n    return color1.g;\n}}\n\nvec4 movingAverageFilter_line_of_sight(vec3 loc, vec3 step)\n{{\n    // Initialise variables\n    vec4 partial_color = vec4(0.0, 0.0, 0.0, 0.0);\n\n    for ( int i=1; i<=u_filter_arm; i++ )\n    {{\n        partial_color += $sample(u_volumetex, loc-i*step);\n        partial_color += $sample(u_volumetex, loc+i*step);\n    }}\n\n    partial_color += $sample(u_volumetex, loc);\n\n    // Evaluate mean\n    partial_color *= u_filter_coeff;\n\n    return partial_color;\n}}\n\nvec4 Gaussian_5(vec4 color_original, vec3 loc, vec3 direction) {{\n  vec4 color = vec4(0.0);\n  vec3 off1 = 1.3333333333333333 * direction;\n  color += color_original * 0.29411764705882354;\n  color += $sample(u_volumetex, loc + (off1 * u_resolution)) * 0.35294117647058826;\n  color += $sample(u_volumetex, loc - (off1 * u_resolution)) * 0.35294117647058826;\n  return color;\n}}\n\nvec4 Gaussian_9(vec4 color_original, vec3 loc, vec3 direction)\n{{\n    vec4 color = vec4(0.0);\n    vec3 off1 = 1.3846153846 * direction;\n    vec3 off2 = 3.2307692308 * direction;\n    color += color_original * 0.2270270270;\n    color += $sample(u_volumetex, loc + (off1 * u_resolution)) * 0.3162162162;\n    color += $sample(u_volumetex, loc - (off1 * u_resolution)) * 0.3162162162;\n    color += $sample(u_volumetex, loc + (off2 * u_resolution)) * 0.0702702703;\n    color += $sample(u_volumetex, loc - (off2 * u_resolution)) * 0.0702702703;\n    return color;\n}}\n\nvec4 Gaussian_13(vec4 color_original, vec3 loc, vec3 direction) {{\n  vec4 color = vec4(0.0);\n  vec3 off1 = 1.411764705882353 * direction;\n  vec3 off2 = 3.2941176470588234 * direction;\n  vec3 off3 = 5.176470588235294 * direction;\n  color += color_original * 0.1964825501511404;\n  color += $sample(u_volumetex, loc + (off1 * u_resolution)) * 0.2969069646728344;\n  color += $sample(u_volumetex, loc - (off1 * u_resolution)) * 0.2969069646728344;\n  color += $sample(u_volumetex, loc + (off2 * u_resolution)) * 0.09447039785044732;\n  color += $sample(u_volumetex, loc - (off2 * u_resolution)) * 0.09447039785044732;\n  color += $sample(u_volumetex, loc + (off3 * u_resolution)) * 0.010381362401148057;\n  color += $sample(u_volumetex, loc - (off3 * u_resolution)) * 0.010381362401148057;\n  return color;\n}}\n\n// ----------------------------------------------------------------\n// ----------------------------------------------------------------\n// Edge detection Pass\n// (adapted from https://www.shadertoy.com/view/MscSzf#)\n// ----------------------------------------------------------------\nfloat checkSame(vec4 center, vec4 sample, vec3 resolution) {{\n    vec2 centerNormal = center.xy;\n    float centerDepth = center.z;\n    vec2 sampleNormal = sample.xy;\n    float sampleDepth = sample.z;\n\n    vec2 sensitivity = (vec2(0.3, 1.5) * resolution.y / 50.0);\n\n    vec2 diffNormal = abs(centerNormal - sampleNormal) * sensitivity.x;\n    bool isSameNormal = (diffNormal.x + diffNormal.y) < 0.1;\n    float diffDepth = abs(centerDepth - sampleDepth) * sensitivity.y;\n    bool isSameDepth = diffDepth < 0.1;\n\n    return (isSameNormal && isSameDepth) ? 1.0 : 0.0;\n}}\n\nvec4 edge_detection(vec4 color_original, vec3 loc, vec3 step, vec3 resolution) {{\n\n    vec4 sample1 = $sample(u_volumetex, loc + (vec3(1., 1., 0.) / resolution));\n    vec4 sample2 = $sample(u_volumetex, loc + (vec3(-1., -1., 0.) / resolution));\n    vec4 sample3 = $sample(u_volumetex, loc + (vec3(-1., 1., 0.) / resolution));\n    vec4 sample4 = $sample(u_volumetex, loc + (vec3(1., -1., 0.) / resolution));\n\n    float edge = checkSame(sample1, sample2, resolution) *\n                 checkSame(sample3, sample4, resolution);\n\n    return vec4(color_original.rgb, 1-edge);\n}}\n// ----------------------------------------------------------------\n// ----------------------------------------------------------------\n\n// Used with iso surface\nvec4 calculateColor(vec4 betterColor, vec3 loc, vec3 step)\n{{\n    // Calculate color by incorporating lighting\n    vec4 color1;\n    vec4 color2;\n\n    // View direction\n    vec3 V = normalize(view_ray);\n\n    // calculate normal vector from gradient\n    vec3 N; // normal\n    color1 = $sample( u_volumetex, loc+vec3(-step[0],0.0,0.0) );\n    color2 = $sample( u_volumetex, loc+vec3(step[0],0.0,0.0) );\n    N[0] = colorToVal(color1) - colorToVal(color2);\n    betterColor = max(max(color1, color2),betterColor);\n    color1 = $sample( u_volumetex, loc+vec3(0.0,-step[1],0.0) );\n    color2 = $sample( u_volumetex, loc+vec3(0.0,step[1],0.0) );\n    N[1] = colorToVal(color1) - colorToVal(color2);\n    betterColor = max(max(color1, color2),betterColor);\n    color1 = $sample( u_volumetex, loc+vec3(0.0,0.0,-step[2]) );\n    color2 = $sample( u_volumetex, loc+vec3(0.0,0.0,step[2]) );\n    N[2] = colorToVal(color1) - colorToVal(color2);\n    betterColor = max(max(color1, color2),betterColor);\n    float gm = length(N); // gradient magnitude\n    N = normalize(N);\n\n    // Flip normal so it points towards viewer\n    float Nselect = float(dot(N,V) > 0.0);\n    N = (2.0*Nselect - 1.0) * N;  // ==  Nselect * N - (1.0-Nselect)*N;\n\n    // Get color of the texture (albeido)\n    color1 = betterColor;\n    color2 = color1;\n    // todo: parametrise color1_to_color2\n\n    // Init colors\n    vec4 ambient_color = vec4(0.0, 0.0, 0.0, 0.0);\n    vec4 diffuse_color = vec4(0.0, 0.0, 0.0, 0.0);\n    vec4 specular_color = vec4(0.0, 0.0, 0.0, 0.0);\n    vec4 final_color;\n\n    // todo: allow multiple light, define lights on viewvox or subscene\n    int nlights = 1;\n    for (int i=0; i<nlights; i++)\n    {{\n        // Get light direction (make sure to prevent zero devision)\n        vec3 L = normalize(view_ray);  //lightDirs[i];\n        float lightEnabled = float( length(L) > 0.0 );\n        L = normalize(L+(1.0-lightEnabled));\n\n        // Calculate lighting properties\n        float lambertTerm = clamp( dot(N,L), 0.0, 1.0 );\n        vec3 H = normalize(L+V); // Halfway vector\n        float specularTerm = pow( max(dot(H,N),0.0), u_shininess);\n\n        // Calculate mask\n        float mask1 = lightEnabled;\n\n        // Calculate colors\n        ambient_color +=  mask1 * u_ambient;  // * gl_LightSource[i].ambient;\n        diffuse_color +=  mask1 * lambertTerm;\n        specular_color += mask1 * specularTerm * u_specular;\n    }}\n\n    // Calculate final color by componing different components\n    final_color = color2 * ( ambient_color + diffuse_color) + specular_color;\n    final_color.a = color2.a;\n\n    // Done\n    return final_color;\n}}\n\n// for some reason, this has to be the last function in order for the\n// filters to be inserted in the correct place...\n\nvoid main() {{\n    vec3 farpos = v_farpos.xyz / v_farpos.w;\n    vec3 nearpos = v_nearpos.xyz / v_nearpos.w;\n\n    // Calculate unit vector pointing in the view direction through this\n    // fragment.\n    view_ray = normalize(farpos.xyz - nearpos.xyz);\n\n    // Compute the distance to the front surface or near clipping plane\n    float distance = dot(nearpos-v_position, view_ray);\n    distance = max(distance, min((-0.5 - v_position.x) / view_ray.x,\n                            (u_shape.x - 0.5 - v_position.x) / view_ray.x));\n    distance = max(distance, min((-0.5 - v_position.y) / view_ray.y,\n                            (u_shape.y - 0.5 - v_position.y) / view_ray.y));\n    distance = max(distance, min((-0.5 - v_position.z) / view_ray.z,\n                            (u_shape.z - 0.5 - v_position.z) / view_ray.z));\n\n    // Now we have the starting position on the front surface\n    vec3 front = v_position + view_ray * distance;\n\n    // Decide how many steps to take\n    int nsteps = int(-distance / u_relative_step_size + 0.5);\n    if( nsteps < 1 )\n        discard;\n\n    // Get starting location and step vector in texture coordinates\n    vec3 step = ((v_position - front) / u_shape) / nsteps;\n    vec3 start_loc = front / u_shape;\n\n    // For testing: show the number of steps. This helps to establish\n    // whether the rays are correctly oriented\n    //gl_FragColor = vec4(0.0, nsteps / 3.0 / u_shape.x, 1.0, 1.0);\n    //return;\n\n    {before_loop}\n\n    vec3 loc = start_loc;\n    int iter = 0;\n\n\n    float discard_ratio = 1.0 / (u_high_discard_filter_value - u_low_discard_filter_value);\n    float low_discard_ratio = 1.0 / u_low_discard_filter_value;\n\n\n    for (iter=0; iter<nsteps; iter++)\n    {{\n        // Get sample color\n        vec4 color;\n\n        if (u_filter_size == 1)\n            color = $sample(u_volumetex, loc);\n        else {{\n            color = movingAverageFilter_line_of_sight(loc, step);\n        }}\n\n        if (u_use_gaussian_filter==1) {{\n            vec4 temp_color;\n            vec3 direction;\n            if (u_gaussian_filter_size == 5){{\n                // horizontal\n                direction = vec3(1., 0., 0.);\n                temp_color = Gaussian_5(color, loc, direction);\n\n                // vertical\n                direction = vec3(0., 1., 0.);\n                temp_color = Gaussian_5(temp_color, loc, direction);\n\n                // depth\n                direction = vec3(0., 0., 1.);\n                temp_color = Gaussian_5(temp_color, loc, direction);\n            }}\n\n            if (u_gaussian_filter_size == 9){{\n                // horizontal\n                direction = vec3(1., 0., 0.);\n                temp_color = Gaussian_9(color, loc, direction);\n\n                // vertical\n                direction = vec3(0., 1., 0.);\n                temp_color = Gaussian_9(temp_color, loc, direction);\n\n                // depth\n                direction = vec3(0., 0., 1.);\n                temp_color = Gaussian_9(temp_color, loc, direction);\n            }}\n\n            if (u_gaussian_filter_size == 13){{\n                // horizontal\n                direction = vec3(1., 0., 0.);\n                temp_color = Gaussian_13(color, loc, direction);\n\n                // vertical\n                direction = vec3(0., 1., 0.);\n                temp_color = Gaussian_13(temp_color, loc, direction);\n\n                // depth\n                direction = vec3(0., 0., 1.);\n                temp_color = Gaussian_13(temp_color, loc, direction);\n            }}\n            color = temp_color;\n        }}\n\n        float val = color.g;\n\n        // To force activating the uniform - this should be done differently\n        float density_factor = u_density_factor;\n\n        if (u_filter_type == 1) {{\n            // Get rid of very strong signal values\n            if (val > u_high_discard_filter_value)\n            {{\n                val = 0.;\n            }}\n\n            // Don't consider noisy values\n            //if (val < u_volume_mean - 3*u_volume_std)\n            if (val < u_low_discard_filter_value)\n            {{\n                val = 0.;\n            }}\n\n            if (u_low_discard_filter_value == u_high_discard_filter_value)\n            {{\n                if (u_low_discard_filter_value != 0.)\n                {{\n                    val *= low_discard_ratio;\n                }}\n            }}\n            else {{\n                val -= u_low_discard_filter_value;\n                val *= discard_ratio;\n            }}\n        }}\n        else {{\n            if (val > u_high_discard_filter_value)\n            {{\n                val = 0.;\n            }}\n\n            if (val < u_low_discard_filter_value)\n            {{\n                val = 0.;\n            }}\n        }}\n\n        {in_loop}\n\n        // Advance location deeper into the volume\n        loc += step;\n    }}\n\n    {after_loop}\n\n    //gl_FragColor = edge_detection(gl_FragColor, loc, step, u_shape);\n\n    /* Set depth value - from visvis TODO\n    int iter_depth = int(maxi);\n    // Calculate end position in world coordinates\n    vec4 position2 = vertexPosition;\n    position2.xyz += ray*shape*float(iter_depth);\n    // Project to device coordinates and set fragment depth\n    vec4 iproj = gl_ModelViewProjectionMatrix * position2;\n    iproj.z /= iproj.w;\n    gl_FragDepth = (iproj.z+1.0)/2.0;\n    */\n}}\n\n\n"
MIP_SNIPPETS = dict(before_loop='\n        float maxval = -99999.0; // The maximum encountered value\n        int maxi = 0;  // Where the maximum value was encountered\n        ', in_loop='\n        if( val > maxval ) {\n            maxval = val;\n            maxi = iter;\n        }\n        ', after_loop='\n        // Refine search for max value\n        loc = start_loc + step * (float(maxi) - 0.5);\n\n        for (int i=0; i<10; i++) {\n            maxval = max(maxval, $sample(u_volumetex, loc).g);\n            loc += step * 0.1;\n        }\n\n        if (maxval > u_high_discard_filter_value || maxval < u_low_discard_filter_value)\n        {{\n            maxval = 0.;\n        }}\n\n        // Color is associated to voxel intensity\n        if (u_color_method == 0) {\n            gl_FragColor = $cmap(maxval);\n            //gl_FragColor.a = maxval;\n        }\n        else{\n            // Color is associated to redshift/velocity\n            if (u_color_method == 1) {\n                gl_FragColor = $cmap(loc.y);\n\n                //if (maxval == 0)\n                    gl_FragColor.a = maxval;\n            }\n            // Color is associated to RGB cube\n            else {\n                if (u_color_method == 2) {\n                    gl_FragColor.r = loc.y;\n                    gl_FragColor.g = loc.z;\n                    gl_FragColor.b = loc.x;\n                    gl_FragColor.a = maxval;\n                }\n                // Case 4: Mom2\n                // TODO: verify implementation of MIP-mom2.\n                else {\n                   gl_FragColor = $cmap((maxval * ((maxval - loc.y) * (maxval - loc.y))) / maxval);\n                }\n            }\n        }\n\n        ')
MIP_FRAG_SHADER = FRAG_SHADER.format(**MIP_SNIPPETS)
LMIP_SNIPPETS = dict(before_loop='\n        float maxval = -99999.0; // The maximum encountered value\n        float local_maxval = -99999.0; // The local maximum encountered value\n        int maxi = 0;  // Where the maximum value was encountered\n        int local_maxi = 0;  // Where the local maximum value was encountered\n        bool local_max_found = false;\n        ', in_loop='\n        if( val > u_threshold && !local_max_found ) {\n            local_maxval = val;\n            local_maxi = iter;\n            local_max_found = true;\n        }\n\n        if( val > maxval) {\n            maxval = val;\n            maxi = iter;\n        }\n        ', after_loop='\n        if (!local_max_found) {\n            local_maxval = maxval;\n            local_maxi = maxi;\n        }\n\n        // Refine search for max value\n        loc = start_loc + step * (float(local_maxi) - 0.5);\n        for (int i=0; i<10; i++) {\n            local_maxval = max(local_maxval, $sample(u_volumetex, loc).g);\n            loc += step * 0.1;\n        }\n\n        if (local_maxval > u_high_discard_filter_value) {\n            local_maxval = 0.;\n        }\n\n        if (local_maxval < u_low_discard_filter_value) {\n            local_maxval = 0.;\n        }\n\n        // Color is associated to voxel intensity\n        if (u_color_method == 0) {\n            gl_FragColor = $cmap(local_maxval);\n            gl_FragColor.a = local_maxval;\n        }\n        // Color is associated to redshift/velocity\n        else {\n            gl_FragColor = $cmap(loc.y);\n            gl_FragColor.a = local_maxval;\n        }\n        ')
LMIP_FRAG_SHADER = FRAG_SHADER.format(**LMIP_SNIPPETS)
TRANSLUCENT_SNIPPETS = dict(before_loop='\n        vec4 integrated_color = vec4(0., 0., 0., 0.);\n        float mom0 = 0.;\n        float mom1 = 0.;\n        float ratio = 1/nsteps; // final average\n        float a1 = 0.;\n        float a2 = 0.;\n        ', in_loop='\n            float alpha;\n            // Case 1: Color is associated to voxel intensity\n            if (u_color_method == 0) {\n                /*color = $cmap(val);\n                a1 = integrated_color.a;\n                a2 = val * density_factor * (1 - a1);\n\n                alpha = max(a1 + a2, 0.001);\n\n                integrated_color *= a1 / alpha;\n                integrated_color += color * a2 / alpha;*/\n\n                color = $cmap(val);\n\n                a1 = integrated_color.a;\n                a2 = val * density_factor * (1 - a1);\n\n                alpha = max(a1 + a2, 0.001);\n\n                integrated_color *= a1 / alpha;\n                integrated_color += color * a2 / alpha;\n\n            }\n            else{\n                // Case 2: Color is associated to redshift/velocity\n                if (u_color_method == 1) {\n                    color = $cmap(loc.y);\n                    a1 = integrated_color.a;\n                    a2 = val * density_factor * (1 - a1);\n\n                    alpha = max(a1 + a2, 0.001);\n\n                    integrated_color *= a1 / alpha;\n                    integrated_color.rgb += color.rgb * a2 / alpha;\n                }\n                // Case 3: Color is associated to RGB cube\n                else {\n                    if (u_color_method == 2){\n                        color.r = loc.y;\n                        color.g = loc.z;\n                        color.b = loc.x;\n                        a1 = integrated_color.a;\n                        a2 = val * density_factor * (1 - a1);\n\n                        alpha = max(a1 + a2, 0.001);\n\n                        integrated_color *= a1 / alpha;\n                        integrated_color.rgb += color.rgb * a2 / alpha;\n                    }\n                    // Case 4: Mom2\n                    // TODO: Finish implementation of mom2 (not correct in its present form).\n                    else {\n                        // mom0\n                        a1 = mom0;\n                        a2 = val * density_factor * (1 - a1);\n\n                        alpha = max(a1 + a2, 0.001);\n\n                        mom0 *= a1 / alpha;\n                        mom0 += val * a2 / alpha;\n\n                        // mom1\n                        a1 = mom1;\n                        a2 = val * density_factor * (1 - a1);\n\n                        alpha = max(a1 + a2, 0.001);\n\n                        mom1 *= a1 / alpha;\n                        mom1 += loc.y * a2 / alpha;\n                    }\n                }\n            }\n\n            integrated_color.a = alpha;\n\n            // stop integrating if the fragment becomes opaque\n            if( alpha > 0.99 ){\n                iter = nsteps;\n            }\n\n        ', after_loop='\n\n        if (u_color_method != 3){\n            gl_FragColor = integrated_color;\n        }\n        else {\n            gl_FragColor = $cmap((mom0  * (mom0-mom1 * mom0-mom1)) / mom0);\n        }\n        ')
TRANSLUCENT_FRAG_SHADER = FRAG_SHADER.format(**TRANSLUCENT_SNIPPETS)
TRANSLUCENT2_SNIPPETS = dict(before_loop='\n        vec4 integrated_color = vec4(0., 0., 0., 0.);\n        float ratio = 1/nsteps; // final average\n        ', in_loop='\n            float alpha;\n            // Case 1: Color is associated to voxel intensity\n            if (u_color_method == 0) {\n                color = $cmap(val);\n                integrated_color = (val * density_factor + integrated_color.a * (1 - density_factor)) * color;\n                alpha = integrated_color.a;\n\n                //alpha = a1+a2;\n                // integrated_color *= a1 / alpha;\n                // integrated_color += color * a2 / alpha;\n            }\n            else{\n                // Case 2: Color is associated to redshift/velocity\n                if (u_color_method == 1) {\n                    color = $cmap(loc.y);\n                    float a1 = integrated_color.a;\n                    float a2 = val * density_factor * (1 - a1);\n\n                    alpha = max(a1 + a2, 0.001);\n\n                    integrated_color *= a1 / alpha;\n                    integrated_color.rgb += color.rgb * a2 / alpha;\n                }\n                // Case 3: Color is associated to RGB cube\n                else {\n                    color.r = loc.x;\n                    color.g = loc.z;\n                    color.b = loc.y;\n                    float a1 = integrated_color.a;\n                    float a2 = val * density_factor * (1 - a1);\n\n                    alpha = max(a1 + a2, 0.001);\n\n                    integrated_color *= a1 / alpha;\n                    integrated_color.rgb += color.rgb * a2 / alpha;\n                }\n            }\n\n            integrated_color.a = alpha;\n\n            // stop integrating if the fragment becomes opaque\n            if( alpha > 0.99 ){\n                iter = nsteps;\n            }\n\n        ', after_loop='\n        gl_FragColor = integrated_color;\n        ')
TRANSLUCENT2_FRAG_SHADER = FRAG_SHADER.format(**TRANSLUCENT2_SNIPPETS)
ADDITIVE_SNIPPETS = dict(before_loop='\n        vec4 integrated_color = vec4(0., 0., 0., 0.);\n        ', in_loop='\n        color = $cmap(val);\n\n        integrated_color = 1.0 - (1.0 - integrated_color) * (1.0 - color);\n        ', after_loop='\n        gl_FragColor = integrated_color;\n        ')
ADDITIVE_FRAG_SHADER = FRAG_SHADER.format(**ADDITIVE_SNIPPETS)
ISO_SNIPPETS = dict(before_loop='\n        vec4 color3 = vec4(0.0);  // final color\n        vec3 dstep = 1.5 / u_shape;  // step to sample derivative\n        gl_FragColor = vec4(0.0);\n    ', in_loop='\n        if (val > u_threshold-0.2) {\n            // Take the last interval in smaller steps\n            vec3 iloc = loc - step;\n            for (int i=0; i<10; i++) {\n                val = $sample(u_volumetex, iloc).g;\n                if (val > u_threshold) {\n                    color = $cmap(val);\n                    gl_FragColor = calculateColor(color, iloc, dstep);\n                    iter = nsteps;\n                    break;\n                }\n                iloc += step * 0.1;\n            }\n        }\n        ', after_loop='\n        ')
ISO_FRAG_SHADER = FRAG_SHADER.format(**ISO_SNIPPETS)
frag_dict = {'mip': MIP_FRAG_SHADER, 
 'lmip': LMIP_FRAG_SHADER, 
 'iso': ISO_FRAG_SHADER, 
 'avip': TRANSLUCENT_FRAG_SHADER, 
 'translucent2': TRANSLUCENT2_FRAG_SHADER, 
 'additive': ADDITIVE_FRAG_SHADER}

class RenderVolumeVisual(Visual):
    __doc__ = " Displays a 3D Volume\n    \n    Parameters\n    ----------\n    vol : ndarray\n        The volume to display. Must be ndim==3.\n    clim : tuple of two floats | None\n        The contrast limits. The values in the volume are mapped to\n        black and white corresponding to these values. Default maps\n        between min and max.\n    method : {'mip', 'avip', 'additive', 'iso'}\n        The render method to use. See corresponding docs for details.\n        Default 'mip'.\n    threshold : float\n        The threshold to use for the isosurafce render method. By default\n        the mean of the given volume is used.\n    relative_step_size : float\n        The relative step size to step through the volume. Default 0.8.\n        Increase to e.g. 1.5 to increase performance, at the cost of\n        quality.\n    cmap : str\n        Colormap to use.\n    emulate_texture : bool\n        Use 2D textures to emulate a 3D texture. OpenGL ES 2.0 compatible,\n        but has lower performance on desktop platforms.\n    "

    def __init__(self, vol, clim=None, method='mip', threshold=None, relative_step_size=0.8, cmap='grays', emulate_texture=False, color_scale='linear', filter_type=0, filter_size=1, use_gaussian_filter=False, gaussian_filter_size=9, density_factor=0.01, color_method='Moment 0', log_scale=0, interpolation='linear'):
        tex_cls = TextureEmulated3D if emulate_texture else Texture3D
        self._vol_shape = ()
        self._clim = None
        self._need_vertex_update = True
        self._cmap = get_colormap(cmap)
        self._vertices = VertexBuffer()
        self._texcoord = VertexBuffer(np.array([
         [
          0, 0, 0],
         [
          1, 0, 0],
         [
          0, 1, 0],
         [
          1, 1, 0],
         [
          0, 0, 1],
         [
          1, 0, 1],
         [
          0, 1, 1],
         [
          1, 1, 1]], dtype=np.float32))
        self._tex = tex_cls((10, 10, 10), interpolation=interpolation, wrapping='clamp_to_edge')
        Visual.__init__(self, vcode=VERT_SHADER, fcode='')
        self.shared_program['u_volumetex'] = self._tex
        self.shared_program['a_position'] = self._vertices
        self.shared_program['a_texcoord'] = self._texcoord
        self._draw_mode = 'triangle_strip'
        self._index_buffer = IndexBuffer()
        self.set_gl_state('translucent', cull_face=False)
        self.set_data(vol, clim)
        self.method = method
        self.relative_step_size = relative_step_size
        self.filter_type = filter_type
        self.filter_size = filter_size
        self.use_gaussian_filter = use_gaussian_filter
        self.gaussian_filter_size = gaussian_filter_size
        self.log_scale = log_scale
        self.density_factor = density_factor
        self.color_method = color_method
        self.threshold = threshold if threshold is not None else vol.mean()
        self.freeze()

    def set_data(self, vol, clim=None):
        """ Set the volume data.

        Parameters
        ----------
        vol : ndarray
            The 3D volume.
        clim : tuple | None
            Colormap limits to use. None will use the min and max values.
        """
        if not isinstance(vol, np.ndarray):
            raise ValueError('Volume visual needs a numpy array.')
        if not (vol.ndim == 3 or vol.ndim == 4 and vol.shape[(-1)] <= 4):
            raise ValueError('Volume visual needs a 3D image.')
        if clim is not None:
            clim = np.array(clim, float)
            if not (clim.ndim == 1 and clim.size == 2):
                raise ValueError('clim must be a 2-element array-like')
            self._clim = tuple(clim)
        if self._clim is None:
            self._clim = (
             np.nanmin(vol), np.nanmax(vol))
        vol = np.flipud(np.array(vol, dtype='float32', copy=False))
        if self._clim[1] == self._clim[0]:
            if self._clim[0] != 0.0:
                vol *= 1.0 / self._clim[0]
        else:
            vol -= self._clim[0]
            vol /= self._clim[1] - self._clim[0]
        if np.isnan(vol).any():
            vol = np.nan_to_num(vol)
        self.high_discard_filter_value = self._clim[1]
        self.low_discard_filter_value = self._clim[0]
        self._tex.set_data(vol)
        self.shared_program['u_shape'] = (vol.shape[2], vol.shape[1],
         vol.shape[0])
        self.shared_program['u_resolution'] = (
         1 / vol.shape[2], 1 / vol.shape[1],
         1 / vol.shape[0])
        shape = vol.shape[:3]
        if self._vol_shape != shape:
            self._vol_shape = shape
            self._need_vertex_update = True
        self._vol_shape = shape
        self._kb_for_texture = np.prod(self._vol_shape) / 1024

    @property
    def interpolation(self):
        """ Current interpolation function.
        """
        return self._tex.interpolation

    @interpolation.setter
    def interpolation(self, interpolation):
        self._tex.interpolation = interpolation

    @property
    def clim(self):
        """ The contrast limits that were applied to the volume data.
        Settable via set_data().
        """
        return self._clim

    @property
    def cmap(self):
        return self._cmap

    @cmap.setter
    def cmap(self, cmap):
        self._cmap = get_colormap(cmap)
        self.shared_program.frag['cmap'] = Function(self._cmap.glsl_map)
        self.update()

    @property
    def method(self):
        """The render method to use

        Current options are:

            * avip: voxel colors are blended along the view ray until
              the result is opaque.
            * mip: maxiumum intensity projection. Cast a ray and display the
              maximum value that was encountered.
            * additive: voxel colors are added along the view ray until
              the result is saturated.
            * iso: isosurface. Cast a ray until a certain threshold is
              encountered. At that location, lighning calculations are
              performed to give the visual appearance of a surface.
        """
        return self._method

    @method.setter
    def method(self, method):
        known_methods = list(frag_dict.keys())
        if method not in known_methods:
            raise ValueError('Volume render method should be in %r, not %r' % (
             known_methods, method))
        self._method = method
        if 'u_threshold' in self.shared_program:
            self.shared_program['u_threshold'] = None
        self.shared_program.frag = frag_dict[method]
        self.shared_program.frag['sampler_type'] = self._tex.glsl_sampler_type
        self.shared_program.frag['sample'] = self._tex.glsl_sample
        self.shared_program.frag['cmap'] = Function(self._cmap.glsl_map)
        self.update()

    @property
    def color_method(self):
        """The way color is associated with voxel

        Current options are:

            * regular: Color is associated to voxel intensity (defined by the VR method)
            * velocity/redshit: Color is associated to depth coordinate
                                and alpha to voxel intensity (defined by the VR method)
        """
        return self._color_method

    @color_method.setter
    def color_method(self, color_method):
        if color_method == 'Moment 0':
            self._color_method = 0
        else:
            if color_method == 'Moment 1':
                self._color_method = 1
            else:
                if color_method == 'rgb_cube':
                    self._color_method = 2
                else:
                    self._color_method = 3
        self.shared_program['u_color_method'] = int(self._color_method)
        self.update()

    @property
    def threshold(self):
        """ The threshold value to apply for the isosurface render method.
            Also used for the lmip transfer function.
        """
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = float(value)
        if 'u_threshold' in self.shared_program:
            self.shared_program['u_threshold'] = self._threshold
        self.update()

    @property
    def color_scale(self):
        return self._color_scale

    @color_scale.setter
    def color_scale(self, color_scale):
        if color_scale == 'linear':
            self._color_scale = 0
        else:
            self._color_scale = 1
        self.shared_program['u_color_scale'] = int(self._color_scale)
        self.update()

    @property
    def log_scale(self):
        return self._log_scale

    @log_scale.setter
    def log_scale(self, log_scale):
        self._log_scale = int(log_scale)
        self.update()

    @property
    def data_min(self):
        return self._data_min

    @data_min.setter
    def data_min(self, data_min):
        self._data_min = 0.0
        self.shared_program['u_data_min'] = float(self._data_min)
        self.update()

    @property
    def data_max(self):
        return self._data_max

    @data_max.setter
    def data_max(self, data_max):
        self._data_max = 0.0
        self.shared_program['u_data_max'] = float(self._data_max)
        self.update()

    @property
    def moving_box_filter(self):
        return self._moving_box_filter

    @moving_box_filter.setter
    def moving_box_filter(self, moving_box_filter):
        self.shared_program['u_moving_box_filter'] = int(self._moving_box_filter)
        self.update()

    @property
    def volume_mean(self):
        return self._volume_mean

    @volume_mean.setter
    def volume_mean(self, volume_mean):
        self._volume_mean = float(volume_mean)
        self._volume_mean -= self._clim[0]
        self._volume_mean /= self._clim[1] - self._clim[0]
        self.shared_program['u_volume_mean'] = self._volume_mean
        self.update()

    @property
    def volume_std(self):
        return self._volume_std

    @volume_std.setter
    def volume_std(self, volume_std):
        self._volume_std = float(volume_std)
        self._volume_std -= self._clim[0]
        self._volume_std /= self._clim[1] - self._clim[0]
        self.shared_program['u_volume_std'] = self._volume_std
        self.update()

    @property
    def volume_madfm(self):
        return self._volume_madfm

    @volume_madfm.setter
    def volume_madfm(self, volume_madfm):
        self._volume_madfm = float(volume_madfm)
        self._volume_madfm -= self._clim[0]
        self._volume_madfm /= self._clim[1] - self._clim[0]
        self.shared_program['u_volume_madfm'] = self._volume_madfm
        self.update()

    @property
    def filter_size(self):
        return self._filter_size

    @filter_size.setter
    def filter_size(self, filter_size):
        self._filter_size = int(filter_size)
        self.shared_program['u_filter_size'] = int(self._filter_size)
        self.shared_program['u_filter_arm'] = int(np.floor(self._filter_size / 2))
        self.shared_program['u_filter_coeff'] = float(1 / self._filter_size)
        self.update()

    @property
    def filter_type(self):
        return self._filter_type

    @filter_type.setter
    def filter_type(self, filter_type):
        if filter_type == 'Rescale':
            self._filter_type = 1
        else:
            self._filter_type = 0
        self.shared_program['u_filter_type'] = int(self._filter_type)
        self.update()

    @property
    def use_gaussian_filter(self):
        return self._use_gaussian_filter

    @use_gaussian_filter.setter
    def use_gaussian_filter(self, use_gaussian_filter):
        self._use_gaussian_filter = int(use_gaussian_filter)
        self.shared_program['u_use_gaussian_filter'] = int(self._use_gaussian_filter)
        self.update()

    @property
    def gaussian_filter_size(self):
        return self._gaussian_filter_size

    @gaussian_filter_size.setter
    def gaussian_filter_size(self, gaussian_filter_size):
        self._gaussian_filter_size = int(gaussian_filter_size)
        self.shared_program['u_gaussian_filter_size'] = int(self._gaussian_filter_size)
        self.update()

    @property
    def high_discard_filter_value(self):
        return self._high_discard_filter_value

    @high_discard_filter_value.setter
    def high_discard_filter_value(self, high_discard_filter_value):
        self._high_discard_filter_value = float(high_discard_filter_value)
        self._high_discard_filter_value -= self._clim[0]
        self._high_discard_filter_value /= self._clim[1] - self._clim[0]
        self.shared_program['u_high_discard_filter_value'] = self._high_discard_filter_value
        self.update()

    @property
    def low_discard_filter_value(self):
        return self._low_discard_filter_value

    @low_discard_filter_value.setter
    def low_discard_filter_value(self, low_discard_filter_value):
        self._low_discard_filter_value = float(low_discard_filter_value)
        self._low_discard_filter_value -= self._clim[0]
        self._low_discard_filter_value /= self._clim[1] - self._clim[0]
        self.shared_program['u_low_discard_filter_value'] = self._low_discard_filter_value
        self.update()

    @property
    def density_factor(self):
        return self._density_factor

    @density_factor.setter
    def density_factor(self, density_factor):
        self._density_factor = float(density_factor)
        self.shared_program['u_density_factor'] = self._density_factor
        self.update()

    @property
    def relative_step_size(self):
        """ The relative step size used during raycasting.
        
        Larger values yield higher performance at reduced quality. If
        set > 2.0 the ray skips entire voxels. Recommended values are
        between 0.5 and 1.5. The amount of quality degradation depends
        on the render method.
        """
        return self._relative_step_size

    @relative_step_size.setter
    def relative_step_size(self, value):
        value = float(value)
        if value < 0.1:
            raise ValueError('relative_step_size cannot be smaller than 0.1')
        self._relative_step_size = value
        self.shared_program['u_relative_step_size'] = value

    def _create_vertex_data(self):
        """ Create and set positions and texture coords from the given shape
        
        We have six faces with 1 quad (2 triangles) each, resulting in
        6*2*3 = 36 vertices in total.
        """
        shape = self._vol_shape
        x0, x1 = -0.5, shape[2] - 0.5
        y0, y1 = -0.5, shape[1] - 0.5
        z0, z1 = -0.5, shape[0] - 0.5
        pos = np.array([
         [
          x0, y0, z0],
         [
          x1, y0, z0],
         [
          x0, y1, z0],
         [
          x1, y1, z0],
         [
          x0, y0, z1],
         [
          x1, y0, z1],
         [
          x0, y1, z1],
         [
          x1, y1, z1]], dtype=np.float32)
        indices = np.array([2, 6, 0, 4, 5, 6, 7, 2, 3, 0, 1, 5, 3, 7], dtype=np.uint32)
        self._vertices.set_data(pos)
        self._index_buffer.set_data(indices)

    def _compute_bounds(self, axis, view):
        return (
         0, self._vol_shape[axis])

    def _prepare_transforms(self, view):
        trs = view.transforms
        view.view_program.vert['transform'] = trs.get_transform()
        view_tr_f = trs.get_transform('visual', 'document')
        view_tr_i = view_tr_f.inverse
        view.view_program.vert['viewtransformf'] = view_tr_f
        view.view_program.vert['viewtransformi'] = view_tr_i

    def _prepare_draw(self, view):
        if self._need_vertex_update:
            self._create_vertex_data()

    def madfm(self, volume):
        return np.median(volume - np.median(volume)) * 1.4826042


RenderVolume = create_visual_node(RenderVolumeVisual)

def get_interpolation_fun():
    return get_interpolation_fun()