from panda3d.core import Shader

class ColorCycle():
    def __init__(self) -> None:
            
        vertex = """
        #version 130

        // Uniform inputs
        uniform mat4 p3d_ModelViewProjectionMatrix;
        uniform mat4 p3d_TextureMatrix;

        // Vertex inputs
        in vec4 p3d_Vertex;
        in vec2 p3d_MultiTexCoord0;

        // Output to fragment shader
        out vec2 texcoord;

        void main() {
        gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
        //texcoord = p3d_MultiTexCoord0*p3d_TextureMatrix;
        texcoord = (p3d_TextureMatrix * vec4(p3d_MultiTexCoord0, 0, 1)).xy;
        }
        """


        fragment = """
        #version 130

        uniform sampler2D p3d_Texture0;
        uniform int osg_FrameNumber;
        uniform float speed;

        // Input from vertex shader
        in vec2 texcoord;


        // Output to the screen
        out vec4 p3d_FragColor;

        vec4 hue_shift(vec4 color, float hue) {
            const vec3 k = vec3(0.57735, 0.57735, 0.57735);
            float cos_rad = cos(hue);
            return vec4(color.rgb * cos_rad + cross(k, color.rgb) * sin(hue) + k * dot(k, color.rgb) * (1.0 - cos_rad), color.a);
        }

        void main() {
        float h = osg_FrameNumber*speed;
        vec4 color = vec4(hue_shift(texture(p3d_Texture0, texcoord), h));
        p3d_FragColor = color.rgba;
        }
        """

        self.SHADER = Shader.make(Shader.SL_GLSL, vertex, fragment)

    def apply_hue_cycle(self, nodepath, rate=0.01):
        nodepath.set_shader(self.SHADER)
        nodepath.set_shader_input('speed', rate)