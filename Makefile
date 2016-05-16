include ../config.h

install:
	$(PYTHON) setup.py install --prefix=$(AMBERHOME) --install-scripts=$(BINDIR)

clean:
	/bin/rm -rf build/

uninstall:
	/bin/rm -f $(BINDIR)/MCPB.py $(BINDIR)/OptC4.py $(BINDIR)/PdbSearcher.py $(BINDIR)/IPMach.py $(BINDIR)/CartHess2FC.py $(BINDIR)/espgen.py

test:
	cp -r $(AMBERHOME)/AmberTools/src/pymsmt/tests/g03/ $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03/ ; \
       cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g03 ; ./Run.pymsmt
	cp -r $(AMBERHOME)/AmberTools/src/pymsmt/tests/g09 $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09/ ; \
       cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/g09 ; ./Run.pymsmt
	cp -r $(AMBERHOME)/AmberTools/src/pymsmt/tests/gms $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms/ ; \
       cd $(AMBERHOME)/AmberTools/test/pymsmt/mcpb/gms ; ./Run.pymsmt

skip:
	@echo ""
	@echo "Skipping installation of pyMSMT."
	@echo ""

