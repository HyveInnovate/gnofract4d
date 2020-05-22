#include <crunch++.h>
#include <memory>

#include "model/image.h"

class testSuite final : public testsuite
{
public:
	void registerTests() final override {
		CRUNCHpp_TEST(testAssertions)
		CRUNCHpp_TEST(testImageResolution)
	}
private:
	void testAssertions()
	{
		assertNotNull(this);
		assertTrue(true);
	}

	void testImageResolution()
	{
		auto im{std::make_unique<image>()};
    	im->set_resolution(640, 480, -1, -1);
		assertEqual(im->totalXres(), 640);
		assertEqual(im->totalYres(), 480);
	}

};

CRUNCHpp_TESTS(testSuite);
