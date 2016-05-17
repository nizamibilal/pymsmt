include ../config.h

install:
	$(PYTHON) setup.py install --prefix=$(AMBERHOME) --install-scripts=$(BINDIR)

installold:
	./setup.sh $(BINDIR) $(PYTHON)

clean:
	/bin/rm -rf build/

cleanold:
	-(find . -name "*.pyc" | /usr/bin/xargs /bin/rm)

uninstall:
	/bin/rm -f $(BINDIR)/MCPB.py $(BINDIR)/PdbSearcher.py $(BINDIR)/CartHess2FC.py $(BINDIR)/espgen.py

uninstallold:
	/bin/rm -f $(BINDIR)/MCPB.py $(BINDIR)/PdbSearcher.py $(BINDIR)/CartHess2FC.py $(BINDIR)/espgen.py \
    /bin/rm -rf $(BINDIR)/api $(BINDIR)/mcpb $(BINDIR)/lib $(BINDIR)/msmtmol $(BINDIR)/ipmach $(BINDIR)/pymsmtexp.py $(BINDIR)/title.py

test:
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03 ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/g03/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03 ; ./Run.pymsmt
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09 ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/g09/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09 ; ./Run.pymsmt
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/gms/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms ; ./Run.pymsmt

testold:
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03_ff12SB ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/g03_ff12SB/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03_ff12SB/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03_ff12SB ; ./Run.pymsmt
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09_ff12SB ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/g09_ff12SB/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09_ff12SB/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09_ff12SB ; ./Run.pymsmt
	mkdir -p $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms_ff12SB ; \
    cp $(AMBERHOME)/AmberTools/src/pymsmt/tests/gms_ff12SB/* $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms_ff12SB/ ; \
    cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms_ff12SB ; ./Run.pymsmt

skip:
	@echo ""
	@echo "Skipping installation of pyMSMT."
	@echo ""

