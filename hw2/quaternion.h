#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

namespace qua
{
    class Quaternion
    {
    public:
        Quaternion(double w, double x, double y, double z):
            _w(w), _x(x), _y(y), _z(z) {}

        double& w()
        {
            return _w;
        }
        double& x()
        {
            return _x;
        }
        double& y()
        {
            return _y;
        }
        double& z()
        {
            return _z;
        }

        double w() const
        {
            return _w;
        }
        double x() const
        {
            return _x;
        }
        double y() const
        {
            return _y;
        }
        double z() const
        {
            return _z;
        }

        double magnitude() const
        {
            return sqrt(_w*_w + _x*_x + _y*_y + _z*_z);
        }

        void normalize()
        {
            double mag = magnitude();
            *this = this->scale(1/mag);
        }

        Quaternion conjugate() const
        {
            return Quaternion(_w, -_x, -_y, -_z);
        }

        Quaternion operator*(const Quaternion& q) const
        {
            return Quaternion(
                _w*q._w - _x*q._x - _y*q._y - _z*q._z,
                _w*q._x + _x*q._w + _y*q._z - _z*q._y,
                _w*q._y - _x*q._z + _y*q._w + _z*q._x,
                _w*q._z + _x*q._y - _y*q._x + _z*q._w
            );
        }

        Quaternion scale(double scalar) const
        {
            return Quaternion(_w * scalar, _x * scalar, _y * scalar, _z * scalar);
        }

    private:
        double _w, _x, _y, _z;
    };
}