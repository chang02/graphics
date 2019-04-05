#include <cmath>
#include <iostream>
#ifdef USING_SSE
#include <xmmintrin.h>
#include <emmintrin.h>
#ifdef __SSE4_1__
#include <smmintrin.h>
#endif
#endif

class Vec3 {
  public:
    union {
      struct { float x, y, z; };
      struct { float r, g, b; };
      float v[3];
#ifdef USING_SSE
      __m128 xyzw;
#endif
    };

  public:
    inline Vec3(float _x = 0.f, float _y = 0.f, float _z = 0.f) : x(_x), y(_y), z(_z) { }
    inline Vec3(float vec[3]) : x(vec[0]), y(vec[1]), z(vec[2]) { }
    inline Vec3(const Vec3& vec) : x(vec.x), y(vec.y), z(vec.z) { }

    inline Vec3 operator+() const { return *this; }
    inline Vec3 operator-() const { return Vec3(-x, -y, -z); }

#ifdef USING_SSE
    inline Vec3(const __m128& _xyzw) : xyzw(_xyzw) { }
    inline Vec3 operator+(const Vec3& lhs) const { return Vec3(_mm_add_ps(xyzw, lhs.xyzw)); }
    inline Vec3 operator-(const Vec3& lhs) const { return Vec3(_mm_sub_ps(xyzw, lhs.xyzw)); }
    inline Vec3 operator*(const float lhs) const { return Vec3(_mm_mul_ps(xyzw, _mm_load1_ps(&lhs))); }
    inline Vec3 operator/(const float lhs) const { return Vec3(_mm_div_ps(xyzw, _mm_load1_ps(&lhs))); }
    inline Vec3& operator+=(const Vec3& lhs) { xyzw = _mm_add_ps(xyzw, lhs.xyzw); return *this; }
    inline Vec3& operator-=(const Vec3& lhs) { xyzw = _mm_sub_ps(xyzw, lhs.xyzw); return *this; }
    inline Vec3& operator*=(const float lhs) { xyzw = _mm_mul_ps(xyzw, _mm_load1_ps(&lhs)); return *this; }
    inline Vec3& operator/=(const float lhs) { xyzw = _mm_sub_ps(xyzw, _mm_load1_ps(&lhs)); return *this; }
    inline float dot(const Vec3& lhs) const {
#ifdef __SSE4_1__
      __m128 res = _mm_dp_ps(xyzw, lhs.xyzw, 0x77);
      return ((Vec3&)res).x;
#else
      __m128 res = _mm_mul_ps(xyzw, lhs.xyzw);
      return res.x + res.y + res.z;
#endif
    }
    inline Vec3 cross(const Vec3& lhs) const {
      __m128 a = _mm_shuffle_ps(xyzw, xyzw, _MM_SHUFFLE(3, 0, 2, 1));
      __m128 b = _mm_shuffle_ps(lhs.xyzw, lhs.xyzw, _MM_SHUFFLE(3, 1, 0, 2));
      a = _mm_mul_ps(a, b);
      __m128 c = _mm_shuffle_ps(lhs.xyzw, lhs.xyzw, _MM_SHUFFLE(3, 0, 2, 1));
      __m128 d = _mm_shuffle_ps(xyzw, xyzw, _MM_SHUFFLE(3, 1, 0, 2));
      c = _mm_mul_ps(c, d);
      return Vec3(_mm_sub_ps(a, c));
    }
    inline void normalise() {
#ifdef __SSE4_1__
      xyzw = _mm_div_ps(xyzw, _mm_sqrt_ps(_mm_dp_ps(xyzw, xyzw, 0x77)));
#else
      float n = dot(*this);
      xyzw = _mm_div_ps(xyzw, _mm_load1_ps(&n));
#endif
    }
    inline Vec3 mul(const Vec3& lhs) const { return Vec3(_mm_mul_ps(xyzw, lhs.xyzw)); }
    inline Vec3 div(const Vec3& lhs) const { return Vec3(_mm_div_ps(xyzw, lhs.xyzw)); }
    inline Vec3 max(const Vec3& lhs) const { return Vec3(_mm_max_ps(xyzw, lhs.xyzw)); }
    inline Vec3 min(const Vec3& lhs) const { return Vec3(_mm_min_ps(xyzw, lhs.xyzw)); }

#else
    inline Vec3 operator+(const Vec3& lhs) const { return Vec3(x + lhs.x, y + lhs.y, z + lhs.z); }
    inline Vec3 operator-(const Vec3& lhs) const { return Vec3(x - lhs.x, y - lhs.y, z - lhs.z); }
    inline Vec3 operator*(const float lhs) const { return Vec3(x * lhs, y * lhs, z * lhs); }
    inline Vec3 operator/(const float lhs) const { return Vec3(x / lhs, y / lhs, z / lhs); }
    inline Vec3& operator+=(const Vec3& lhs) { x += lhs.x; y += lhs.y; z += lhs.z; return *this; }
    inline Vec3& operator-=(const Vec3& lhs) { x -= lhs.x; y -= lhs.y; z -= lhs.z; return *this; }
    inline Vec3& operator*=(const float lhs) { x *= lhs; y *= lhs; z *= lhs; return *this; }
    inline Vec3& operator/=(const float lhs) { x /= lhs; y /= lhs; z /= lhs; return *this; }
    inline float dot(const Vec3& lhs) const { return x*lhs.x + y*lhs.y + z*lhs.z; }
    inline Vec3 cross(const Vec3& lhs) const { return Vec3(y * lhs.z - z * lhs.y, z * lhs.x - x * lhs.z, x * lhs.y - y * lhs.x);}
    inline void normalise() { float n = sqrt(x*x + y*y + z*z); x /= n; y /= n; z /= n; }
    inline Vec3 mul(const Vec3& lhs) const { return Vec3(x*lhs.x, y*lhs.y, z*lhs.z); }
    inline Vec3 div(const Vec3& lhs) const { return Vec3(x/lhs.x, y/lhs.y, z/lhs.z); }
    inline Vec3 max(const Vec3& lhs) const { return Vec3(std::max(x, lhs.x), std::max(y, lhs.y), std::max(z, lhs.z)); }
    inline Vec3 min(const Vec3& lhs) const { return Vec3(std::min(x, lhs.x), std::min(y, lhs.y), std::min(z, lhs.z)); }
#endif
    inline float norm2() const { return dot(*this); }
    inline float norm() const { return sqrt(norm2()); }
    inline Vec3 unit() const { Vec3 res(*this); res.normalise(); return res; }
};

#ifdef USING_SSE
inline Vec3 operator*(const float rhs, const Vec3& lhs) { return Vec3(_mm_mul_ps(lhs.xyzw, _mm_load1_ps(&rhs))); }
#else
inline Vec3 operator*(const float rhs, const Vec3& lhs) { return lhs * rhs; }
#endif

std::ostream& operator<<(std::ostream& os, const Vec3& vec) {
  os << '(' << vec.x << ',' << vec.y << ',' << vec.z << ')'; 
  return os;
}